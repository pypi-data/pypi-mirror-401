from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class AutomationTriggerPayload(TypedDict, total=False):
    """
    Type hints for system/automation_trigger payload fields.
    
    Trigger for automation stitches.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.automation-stitch.AutomationStitchEndpoint` (via: stitch-name)

    **Usage:**
        payload: AutomationTriggerPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Name. | MaxLen: 35
    description: str  # Description. | MaxLen: 255
    trigger_type: Literal["event-based", "scheduled"]  # Trigger type. | Default: event-based
    event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"]  # Event type. | Default: ioc
    vdom: list[dict[str, Any]]  # Virtual domain(s) that this trigger is valid for.
    license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"]  # License type. | Default: forticare-support
    report_type: Literal["posture", "coverage", "optimization", "any"]  # Security Rating report. | Default: posture
    stitch_name: str  # Triggering stitch name. | MaxLen: 35
    logid: list[dict[str, Any]]  # Log IDs to trigger event.
    trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"]  # Scheduled trigger frequency (default = daily). | Default: daily
    trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]  # Day of week for trigger.
    trigger_day: int  # Day within a month to trigger. | Default: 1 | Min: 1 | Max: 31
    trigger_hour: int  # Hour of the day on which to trigger | Default: 0 | Min: 0 | Max: 23
    trigger_minute: int  # Minute of the hour on which to trigger | Default: 0 | Min: 0 | Max: 59
    trigger_datetime: str  # Trigger date and time (YYYY-MM-DD HH:MM:SS). | Default: 0000-00-00 00:00:00
    fields: list[dict[str, Any]]  # Customized trigger field settings.
    faz_event_name: str  # FortiAnalyzer event handler name. | MaxLen: 255
    faz_event_severity: str  # FortiAnalyzer event severity. | MaxLen: 255
    faz_event_tags: str  # FortiAnalyzer event tags. | MaxLen: 255
    serial: str  # Fabric connector serial number. | MaxLen: 255
    fabric_event_name: str  # Fabric connector event handler name. | MaxLen: 255
    fabric_event_severity: str  # Fabric connector event severity. | MaxLen: 255

# Nested TypedDicts for table field children (dict mode)

class AutomationTriggerVdomItem(TypedDict):
    """Type hints for vdom table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Virtual domain name. | MaxLen: 79


class AutomationTriggerLogidItem(TypedDict):
    """Type hints for logid table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Log ID. | Default: 0 | Min: 1 | Max: 65535


class AutomationTriggerFieldsItem(TypedDict):
    """Type hints for fields table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Entry ID. | Default: 0 | Min: 0 | Max: 4294967295
    name: str  # Name. | MaxLen: 35
    value: str  # Value. | MaxLen: 63


# Nested classes for table field children (object mode)

@final
class AutomationTriggerVdomObject:
    """Typed object for vdom table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Virtual domain name. | MaxLen: 79
    name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class AutomationTriggerLogidObject:
    """Typed object for logid table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Log ID. | Default: 0 | Min: 1 | Max: 65535
    id: int
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class AutomationTriggerFieldsObject:
    """Typed object for fields table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Entry ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # Name. | MaxLen: 35
    name: str
    # Value. | MaxLen: 63
    value: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class AutomationTriggerResponse(TypedDict):
    """
    Type hints for system/automation_trigger API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Name. | MaxLen: 35
    description: str  # Description. | MaxLen: 255
    trigger_type: Literal["event-based", "scheduled"]  # Trigger type. | Default: event-based
    event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"]  # Event type. | Default: ioc
    vdom: list[AutomationTriggerVdomItem]  # Virtual domain(s) that this trigger is valid for.
    license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"]  # License type. | Default: forticare-support
    report_type: Literal["posture", "coverage", "optimization", "any"]  # Security Rating report. | Default: posture
    stitch_name: str  # Triggering stitch name. | MaxLen: 35
    logid: list[AutomationTriggerLogidItem]  # Log IDs to trigger event.
    trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"]  # Scheduled trigger frequency (default = daily). | Default: daily
    trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]  # Day of week for trigger.
    trigger_day: int  # Day within a month to trigger. | Default: 1 | Min: 1 | Max: 31
    trigger_hour: int  # Hour of the day on which to trigger | Default: 0 | Min: 0 | Max: 23
    trigger_minute: int  # Minute of the hour on which to trigger | Default: 0 | Min: 0 | Max: 59
    trigger_datetime: str  # Trigger date and time (YYYY-MM-DD HH:MM:SS). | Default: 0000-00-00 00:00:00
    fields: list[AutomationTriggerFieldsItem]  # Customized trigger field settings.
    faz_event_name: str  # FortiAnalyzer event handler name. | MaxLen: 255
    faz_event_severity: str  # FortiAnalyzer event severity. | MaxLen: 255
    faz_event_tags: str  # FortiAnalyzer event tags. | MaxLen: 255
    serial: str  # Fabric connector serial number. | MaxLen: 255
    fabric_event_name: str  # Fabric connector event handler name. | MaxLen: 255
    fabric_event_severity: str  # Fabric connector event severity. | MaxLen: 255


@final
class AutomationTriggerObject:
    """Typed FortiObject for system/automation_trigger with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Name. | MaxLen: 35
    name: str
    # Description. | MaxLen: 255
    description: str
    # Trigger type. | Default: event-based
    trigger_type: Literal["event-based", "scheduled"]
    # Event type. | Default: ioc
    event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"]
    # Virtual domain(s) that this trigger is valid for.
    vdom: list[AutomationTriggerVdomObject]
    # License type. | Default: forticare-support
    license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"]
    # Security Rating report. | Default: posture
    report_type: Literal["posture", "coverage", "optimization", "any"]
    # Triggering stitch name. | MaxLen: 35
    stitch_name: str
    # Log IDs to trigger event.
    logid: list[AutomationTriggerLogidObject]
    # Scheduled trigger frequency (default = daily). | Default: daily
    trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"]
    # Day of week for trigger.
    trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    # Day within a month to trigger. | Default: 1 | Min: 1 | Max: 31
    trigger_day: int
    # Hour of the day on which to trigger (0 - 23, default = 1). | Default: 0 | Min: 0 | Max: 23
    trigger_hour: int
    # Minute of the hour on which to trigger (0 - 59, default = 0) | Default: 0 | Min: 0 | Max: 59
    trigger_minute: int
    # Trigger date and time (YYYY-MM-DD HH:MM:SS). | Default: 0000-00-00 00:00:00
    trigger_datetime: str
    # Customized trigger field settings.
    fields: list[AutomationTriggerFieldsObject]
    # FortiAnalyzer event handler name. | MaxLen: 255
    faz_event_name: str
    # FortiAnalyzer event severity. | MaxLen: 255
    faz_event_severity: str
    # FortiAnalyzer event tags. | MaxLen: 255
    faz_event_tags: str
    # Fabric connector serial number. | MaxLen: 255
    serial: str
    # Fabric connector event handler name. | MaxLen: 255
    fabric_event_name: str
    # Fabric connector event severity. | MaxLen: 255
    fabric_event_severity: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> AutomationTriggerPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class AutomationTrigger:
    """
    Trigger for automation stitches.
    
    Path: system/automation_trigger
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
    ) -> AutomationTriggerResponse: ...
    
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
    ) -> AutomationTriggerResponse: ...
    
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
    ) -> list[AutomationTriggerResponse]: ...
    
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
    ) -> AutomationTriggerObject: ...
    
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
    ) -> AutomationTriggerObject: ...
    
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
    ) -> list[AutomationTriggerObject]: ...
    
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
    ) -> AutomationTriggerResponse: ...
    
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
    ) -> AutomationTriggerResponse: ...
    
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
    ) -> list[AutomationTriggerResponse]: ...
    
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
    ) -> AutomationTriggerObject | list[AutomationTriggerObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationTriggerObject: ...
    
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationTriggerObject: ...
    
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
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
    ) -> AutomationTriggerObject: ...
    
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
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
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

class AutomationTriggerDictMode:
    """AutomationTrigger endpoint for dict response mode (default for this client).
    
    By default returns AutomationTriggerResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return AutomationTriggerObject.
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
    ) -> AutomationTriggerObject: ...
    
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
    ) -> list[AutomationTriggerObject]: ...
    
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
    ) -> AutomationTriggerResponse: ...
    
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
    ) -> list[AutomationTriggerResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationTriggerObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationTriggerObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
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
    ) -> AutomationTriggerObject: ...
    
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
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
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


class AutomationTriggerObjectMode:
    """AutomationTrigger endpoint for object response mode (default for this client).
    
    By default returns AutomationTriggerObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return AutomationTriggerResponse (TypedDict).
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
    ) -> AutomationTriggerResponse: ...
    
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
    ) -> list[AutomationTriggerResponse]: ...
    
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
    ) -> AutomationTriggerObject: ...
    
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
    ) -> list[AutomationTriggerObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationTriggerObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AutomationTriggerObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationTriggerObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AutomationTriggerObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
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
    ) -> AutomationTriggerObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AutomationTriggerObject: ...
    
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
        payload_dict: AutomationTriggerPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        trigger_type: Literal["event-based", "scheduled"] | None = ...,
        event_type: Literal["ioc", "event-log", "reboot", "low-memory", "high-cpu", "license-near-expiry", "local-cert-near-expiry", "ha-failover", "config-change", "security-rating-summary", "virus-ips-db-updated", "faz-event", "incoming-webhook", "fabric-event", "ips-logs", "anomaly-logs", "virus-logs", "ssh-logs", "webfilter-violation", "traffic-violation", "stitch"] | None = ...,
        license_type: Literal["forticare-support", "fortiguard-webfilter", "fortiguard-antispam", "fortiguard-antivirus", "fortiguard-ips", "fortiguard-management", "forticloud", "any"] | None = ...,
        report_type: Literal["posture", "coverage", "optimization", "any"] | None = ...,
        stitch_name: str | None = ...,
        logid: str | list[str] | list[dict[str, Any]] | None = ...,
        trigger_frequency: Literal["hourly", "daily", "weekly", "monthly", "once"] | None = ...,
        trigger_weekday: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        trigger_day: int | None = ...,
        trigger_hour: int | None = ...,
        trigger_minute: int | None = ...,
        trigger_datetime: str | None = ...,
        fields: str | list[str] | list[dict[str, Any]] | None = ...,
        faz_event_name: str | None = ...,
        faz_event_severity: str | None = ...,
        faz_event_tags: str | None = ...,
        serial: str | None = ...,
        fabric_event_name: str | None = ...,
        fabric_event_severity: str | None = ...,
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
    "AutomationTrigger",
    "AutomationTriggerDictMode",
    "AutomationTriggerObjectMode",
    "AutomationTriggerPayload",
    "AutomationTriggerObject",
]