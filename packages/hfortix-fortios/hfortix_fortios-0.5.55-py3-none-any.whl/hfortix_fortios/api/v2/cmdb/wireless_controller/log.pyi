from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class LogPayload(TypedDict, total=False):
    """
    Type hints for wireless_controller/log payload fields.
    
    Configure wireless controller event log filters.
    
    **Usage:**
        payload: LogPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    status: Literal["enable", "disable"]  # Enable/disable wireless event logging. | Default: enable
    addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log address group message | Default: notification
    ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log BLE detection message | Default: notification
    clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log client load balancing | Default: notification
    dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log DHCP starvation event | Default: notification
    led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log LED schedule event me | Default: notification
    radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log radio event message. | Default: notification
    rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log rogue AP event messag | Default: notification
    sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log station event message | Default: notification
    sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log station locate messag | Default: notification
    wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log WIDS message. | Default: notification
    wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log WTP event message. | Default: notification
    wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log FAP fips event messag | Default: notification

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class LogResponse(TypedDict):
    """
    Type hints for wireless_controller/log API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    status: Literal["enable", "disable"]  # Enable/disable wireless event logging. | Default: enable
    addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log address group message | Default: notification
    ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log BLE detection message | Default: notification
    clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log client load balancing | Default: notification
    dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log DHCP starvation event | Default: notification
    led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log LED schedule event me | Default: notification
    radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log radio event message. | Default: notification
    rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log rogue AP event messag | Default: notification
    sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log station event message | Default: notification
    sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log station locate messag | Default: notification
    wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log WIDS message. | Default: notification
    wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log WTP event message. | Default: notification
    wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]  # Lowest severity level to log FAP fips event messag | Default: notification


@final
class LogObject:
    """Typed FortiObject for wireless_controller/log with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Enable/disable wireless event logging. | Default: enable
    status: Literal["enable", "disable"]
    # Lowest severity level to log address group message. | Default: notification
    addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log BLE detection message. | Default: notification
    ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log client load balancing message. | Default: notification
    clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log DHCP starvation event message. | Default: notification
    dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log LED schedule event message. | Default: notification
    led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log radio event message. | Default: notification
    radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log rogue AP event message. | Default: notification
    rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log station event message. | Default: notification
    sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log station locate message. | Default: notification
    sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log WIDS message. | Default: notification
    wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log WTP event message. | Default: notification
    wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    # Lowest severity level to log FAP fips event message. | Default: notification
    wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> LogPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Log:
    """
    Configure wireless controller event log filters.
    
    Path: wireless_controller/log
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
    ) -> LogResponse: ...
    
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
    ) -> LogResponse: ...
    
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
    ) -> LogResponse: ...
    
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
    ) -> LogObject: ...
    
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
    ) -> LogObject: ...
    
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
    ) -> LogObject: ...
    
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
    ) -> LogResponse: ...
    
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
    ) -> LogResponse: ...
    
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
    ) -> LogResponse: ...
    
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
    ) -> LogObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LogObject: ...
    
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
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
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
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

class LogDictMode:
    """Log endpoint for dict response mode (default for this client).
    
    By default returns LogResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return LogObject.
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
    ) -> LogObject: ...
    
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
    ) -> LogObject: ...
    
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
    ) -> LogResponse: ...
    
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
    ) -> LogResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LogObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
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
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
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


class LogObjectMode:
    """Log endpoint for object response mode (default for this client).
    
    By default returns LogObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return LogResponse (TypedDict).
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
    ) -> LogResponse: ...
    
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
    ) -> LogResponse: ...
    
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
    ) -> LogObject: ...
    
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
    ) -> LogObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LogObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LogObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
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
        payload_dict: LogPayload | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        addrgrp_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        ble_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        clb_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        dhcp_starv_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        led_sched_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        radio_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        rogue_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        sta_locate_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wids_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
        wtp_fips_event_log: Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"] | None = ...,
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
    "Log",
    "LogDictMode",
    "LogObjectMode",
    "LogPayload",
    "LogObject",
]