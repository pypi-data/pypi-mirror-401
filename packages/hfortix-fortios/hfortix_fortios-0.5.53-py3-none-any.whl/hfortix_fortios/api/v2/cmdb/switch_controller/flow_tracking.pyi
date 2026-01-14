from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class FlowTrackingPayload(TypedDict, total=False):
    """
    Type hints for switch_controller/flow_tracking payload fields.
    
    Configure FortiSwitch flow tracking and export via ipfix/netflow.
    
    **Usage:**
        payload: FlowTrackingPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    sample_mode: Literal["local", "perimeter", "device-ingress"]  # Configure sample mode for the flow tracking. | Default: perimeter
    sample_rate: int  # Configure sample rate for the perimeter and device | Default: 512 | Min: 0 | Max: 99999
    format: Literal["netflow1", "netflow5", "netflow9", "ipfix"]  # Configure flow tracking protocol. | Default: netflow9
    collectors: list[dict[str, Any]]  # Configure collectors for the flow.
    level: Literal["vlan", "ip", "port", "proto", "mac"]  # Configure flow tracking level. | Default: ip
    max_export_pkt_size: int  # Configure flow max export packet size | Default: 512 | Min: 512 | Max: 9216
    template_export_period: int  # Configure template export period | Default: 5 | Min: 1 | Max: 60
    timeout_general: int  # Configure flow session general timeout | Default: 3600 | Min: 60 | Max: 604800
    timeout_icmp: int  # Configure flow session ICMP timeout | Default: 300 | Min: 60 | Max: 604800
    timeout_max: int  # Configure flow session max timeout | Default: 604800 | Min: 60 | Max: 604800
    timeout_tcp: int  # Configure flow session TCP timeout | Default: 3600 | Min: 60 | Max: 604800
    timeout_tcp_fin: int  # Configure flow session TCP FIN timeout | Default: 300 | Min: 60 | Max: 604800
    timeout_tcp_rst: int  # Configure flow session TCP RST timeout | Default: 120 | Min: 60 | Max: 604800
    timeout_udp: int  # Configure flow session UDP timeout | Default: 300 | Min: 60 | Max: 604800
    aggregates: list[dict[str, Any]]  # Configure aggregates in which all traffic sessions

# Nested TypedDicts for table field children (dict mode)

class FlowTrackingCollectorsItem(TypedDict):
    """Type hints for collectors table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Collector name. | MaxLen: 63
    ip: str  # Collector IP address. | Default: 0.0.0.0
    port: int  # Collector port number | Default: 0 | Min: 0 | Max: 65535
    transport: Literal["udp", "tcp", "sctp"]  # Collector L4 transport protocol for exporting pack | Default: udp


class FlowTrackingAggregatesItem(TypedDict):
    """Type hints for aggregates table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Aggregate id. | Default: 0 | Min: 0 | Max: 4294967295
    ip: str  # IP address to group all matching traffic sessions | Default: 0.0.0.0 0.0.0.0


# Nested classes for table field children (object mode)

@final
class FlowTrackingCollectorsObject:
    """Typed object for collectors table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Collector name. | MaxLen: 63
    name: str
    # Collector IP address. | Default: 0.0.0.0
    ip: str
    # Collector port number | Default: 0 | Min: 0 | Max: 65535
    port: int
    # Collector L4 transport protocol for exporting packets. | Default: udp
    transport: Literal["udp", "tcp", "sctp"]
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class FlowTrackingAggregatesObject:
    """Typed object for aggregates table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Aggregate id. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # IP address to group all matching traffic sessions to a flow. | Default: 0.0.0.0 0.0.0.0
    ip: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class FlowTrackingResponse(TypedDict):
    """
    Type hints for switch_controller/flow_tracking API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    sample_mode: Literal["local", "perimeter", "device-ingress"]  # Configure sample mode for the flow tracking. | Default: perimeter
    sample_rate: int  # Configure sample rate for the perimeter and device | Default: 512 | Min: 0 | Max: 99999
    format: Literal["netflow1", "netflow5", "netflow9", "ipfix"]  # Configure flow tracking protocol. | Default: netflow9
    collectors: list[FlowTrackingCollectorsItem]  # Configure collectors for the flow.
    level: Literal["vlan", "ip", "port", "proto", "mac"]  # Configure flow tracking level. | Default: ip
    max_export_pkt_size: int  # Configure flow max export packet size | Default: 512 | Min: 512 | Max: 9216
    template_export_period: int  # Configure template export period | Default: 5 | Min: 1 | Max: 60
    timeout_general: int  # Configure flow session general timeout | Default: 3600 | Min: 60 | Max: 604800
    timeout_icmp: int  # Configure flow session ICMP timeout | Default: 300 | Min: 60 | Max: 604800
    timeout_max: int  # Configure flow session max timeout | Default: 604800 | Min: 60 | Max: 604800
    timeout_tcp: int  # Configure flow session TCP timeout | Default: 3600 | Min: 60 | Max: 604800
    timeout_tcp_fin: int  # Configure flow session TCP FIN timeout | Default: 300 | Min: 60 | Max: 604800
    timeout_tcp_rst: int  # Configure flow session TCP RST timeout | Default: 120 | Min: 60 | Max: 604800
    timeout_udp: int  # Configure flow session UDP timeout | Default: 300 | Min: 60 | Max: 604800
    aggregates: list[FlowTrackingAggregatesItem]  # Configure aggregates in which all traffic sessions


@final
class FlowTrackingObject:
    """Typed FortiObject for switch_controller/flow_tracking with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Configure sample mode for the flow tracking. | Default: perimeter
    sample_mode: Literal["local", "perimeter", "device-ingress"]
    # Configure sample rate for the perimeter and device-ingress s | Default: 512 | Min: 0 | Max: 99999
    sample_rate: int
    # Configure flow tracking protocol. | Default: netflow9
    format: Literal["netflow1", "netflow5", "netflow9", "ipfix"]
    # Configure collectors for the flow.
    collectors: list[FlowTrackingCollectorsObject]
    # Configure flow tracking level. | Default: ip
    level: Literal["vlan", "ip", "port", "proto", "mac"]
    # Configure flow max export packet size | Default: 512 | Min: 512 | Max: 9216
    max_export_pkt_size: int
    # Configure template export period (1-60, default=5 minutes). | Default: 5 | Min: 1 | Max: 60
    template_export_period: int
    # Configure flow session general timeout | Default: 3600 | Min: 60 | Max: 604800
    timeout_general: int
    # Configure flow session ICMP timeout | Default: 300 | Min: 60 | Max: 604800
    timeout_icmp: int
    # Configure flow session max timeout | Default: 604800 | Min: 60 | Max: 604800
    timeout_max: int
    # Configure flow session TCP timeout | Default: 3600 | Min: 60 | Max: 604800
    timeout_tcp: int
    # Configure flow session TCP FIN timeout | Default: 300 | Min: 60 | Max: 604800
    timeout_tcp_fin: int
    # Configure flow session TCP RST timeout | Default: 120 | Min: 60 | Max: 604800
    timeout_tcp_rst: int
    # Configure flow session UDP timeout | Default: 300 | Min: 60 | Max: 604800
    timeout_udp: int
    # Configure aggregates in which all traffic sessions matching
    aggregates: list[FlowTrackingAggregatesObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> FlowTrackingPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class FlowTracking:
    """
    Configure FortiSwitch flow tracking and export via ipfix/netflow.
    
    Path: switch_controller/flow_tracking
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
    ) -> FlowTrackingResponse: ...
    
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
    ) -> FlowTrackingResponse: ...
    
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
    ) -> FlowTrackingResponse: ...
    
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
    ) -> FlowTrackingObject: ...
    
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
    ) -> FlowTrackingObject: ...
    
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
    ) -> FlowTrackingObject: ...
    
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
    ) -> FlowTrackingResponse: ...
    
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
    ) -> FlowTrackingResponse: ...
    
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
    ) -> FlowTrackingResponse: ...
    
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
    ) -> FlowTrackingObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FlowTrackingObject: ...
    
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
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

class FlowTrackingDictMode:
    """FlowTracking endpoint for dict response mode (default for this client).
    
    By default returns FlowTrackingResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return FlowTrackingObject.
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
    ) -> FlowTrackingObject: ...
    
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
    ) -> FlowTrackingObject: ...
    
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
    ) -> FlowTrackingResponse: ...
    
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
    ) -> FlowTrackingResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FlowTrackingObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
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


class FlowTrackingObjectMode:
    """FlowTracking endpoint for object response mode (default for this client).
    
    By default returns FlowTrackingObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return FlowTrackingResponse (TypedDict).
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
    ) -> FlowTrackingResponse: ...
    
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
    ) -> FlowTrackingResponse: ...
    
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
    ) -> FlowTrackingObject: ...
    
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
    ) -> FlowTrackingObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FlowTrackingObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FlowTrackingObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
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
        payload_dict: FlowTrackingPayload | None = ...,
        sample_mode: Literal["local", "perimeter", "device-ingress"] | None = ...,
        sample_rate: int | None = ...,
        format: Literal["netflow1", "netflow5", "netflow9", "ipfix"] | None = ...,
        collectors: str | list[str] | list[dict[str, Any]] | None = ...,
        level: Literal["vlan", "ip", "port", "proto", "mac"] | None = ...,
        max_export_pkt_size: int | None = ...,
        template_export_period: int | None = ...,
        timeout_general: int | None = ...,
        timeout_icmp: int | None = ...,
        timeout_max: int | None = ...,
        timeout_tcp: int | None = ...,
        timeout_tcp_fin: int | None = ...,
        timeout_tcp_rst: int | None = ...,
        timeout_udp: int | None = ...,
        aggregates: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "FlowTracking",
    "FlowTrackingDictMode",
    "FlowTrackingObjectMode",
    "FlowTrackingPayload",
    "FlowTrackingObject",
]