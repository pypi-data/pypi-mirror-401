from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class TrafficShaperPayload(TypedDict, total=False):
    """
    Type hints for firewall/shaper/traffic_shaper payload fields.
    
    Configure shared traffic shaper.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.firewall.traffic-class.TrafficClassEndpoint` (via: exceed-class-id)

    **Usage:**
        payload: TrafficShaperPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Traffic shaper name. | MaxLen: 35
    guaranteed_bandwidth: int  # Amount of bandwidth guaranteed for this shaper | Default: 0 | Min: 0 | Max: 80000000
    maximum_bandwidth: int  # Upper bandwidth limit enforced by this shaper | Default: 0 | Min: 0 | Max: 80000000
    bandwidth_unit: Literal["kbps", "mbps", "gbps"]  # Unit of measurement for guaranteed and maximum ban | Default: kbps
    priority: Literal["low", "medium", "high"]  # Higher priority traffic is more likely to be forwa | Default: high
    per_policy: Literal["disable", "enable"]  # Enable/disable applying a separate shaper for each | Default: disable
    diffserv: Literal["enable", "disable"]  # Enable/disable changing the DiffServ setting appli | Default: disable
    diffservcode: str  # DiffServ setting to be applied to traffic accepted
    dscp_marking_method: Literal["multi-stage", "static"]  # Select DSCP marking method. | Default: static
    exceed_bandwidth: int  # Exceed bandwidth used for DSCP/VLAN CoS multi-stag | Default: 0 | Min: 0 | Max: 80000000
    exceed_dscp: str  # DSCP mark for traffic in guaranteed-bandwidth and
    maximum_dscp: str  # DSCP mark for traffic in exceed-bandwidth and maxi
    cos_marking: Literal["enable", "disable"]  # Enable/disable VLAN CoS marking. | Default: disable
    cos_marking_method: Literal["multi-stage", "static"]  # Select VLAN CoS marking method. | Default: static
    cos: str  # VLAN CoS mark.
    exceed_cos: str  # VLAN CoS mark for traffic in
    maximum_cos: str  # VLAN CoS mark for traffic in
    overhead: int  # Per-packet size overhead used in rate computations | Default: 0 | Min: 0 | Max: 100
    exceed_class_id: int  # Class ID for traffic in guaranteed-bandwidth and m | Default: 0 | Min: 0 | Max: 4294967295

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class TrafficShaperResponse(TypedDict):
    """
    Type hints for firewall/shaper/traffic_shaper API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Traffic shaper name. | MaxLen: 35
    guaranteed_bandwidth: int  # Amount of bandwidth guaranteed for this shaper | Default: 0 | Min: 0 | Max: 80000000
    maximum_bandwidth: int  # Upper bandwidth limit enforced by this shaper | Default: 0 | Min: 0 | Max: 80000000
    bandwidth_unit: Literal["kbps", "mbps", "gbps"]  # Unit of measurement for guaranteed and maximum ban | Default: kbps
    priority: Literal["low", "medium", "high"]  # Higher priority traffic is more likely to be forwa | Default: high
    per_policy: Literal["disable", "enable"]  # Enable/disable applying a separate shaper for each | Default: disable
    diffserv: Literal["enable", "disable"]  # Enable/disable changing the DiffServ setting appli | Default: disable
    diffservcode: str  # DiffServ setting to be applied to traffic accepted
    dscp_marking_method: Literal["multi-stage", "static"]  # Select DSCP marking method. | Default: static
    exceed_bandwidth: int  # Exceed bandwidth used for DSCP/VLAN CoS multi-stag | Default: 0 | Min: 0 | Max: 80000000
    exceed_dscp: str  # DSCP mark for traffic in guaranteed-bandwidth and
    maximum_dscp: str  # DSCP mark for traffic in exceed-bandwidth and maxi
    cos_marking: Literal["enable", "disable"]  # Enable/disable VLAN CoS marking. | Default: disable
    cos_marking_method: Literal["multi-stage", "static"]  # Select VLAN CoS marking method. | Default: static
    cos: str  # VLAN CoS mark.
    exceed_cos: str  # VLAN CoS mark for traffic in
    maximum_cos: str  # VLAN CoS mark for traffic in
    overhead: int  # Per-packet size overhead used in rate computations | Default: 0 | Min: 0 | Max: 100
    exceed_class_id: int  # Class ID for traffic in guaranteed-bandwidth and m | Default: 0 | Min: 0 | Max: 4294967295


@final
class TrafficShaperObject:
    """Typed FortiObject for firewall/shaper/traffic_shaper with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Traffic shaper name. | MaxLen: 35
    name: str
    # Amount of bandwidth guaranteed for this shaper | Default: 0 | Min: 0 | Max: 80000000
    guaranteed_bandwidth: int
    # Upper bandwidth limit enforced by this shaper (0 - 80000000) | Default: 0 | Min: 0 | Max: 80000000
    maximum_bandwidth: int
    # Unit of measurement for guaranteed and maximum bandwidth for | Default: kbps
    bandwidth_unit: Literal["kbps", "mbps", "gbps"]
    # Higher priority traffic is more likely to be forwarded witho | Default: high
    priority: Literal["low", "medium", "high"]
    # Enable/disable applying a separate shaper for each policy. F | Default: disable
    per_policy: Literal["disable", "enable"]
    # Enable/disable changing the DiffServ setting applied to traf | Default: disable
    diffserv: Literal["enable", "disable"]
    # DiffServ setting to be applied to traffic accepted by this s
    diffservcode: str
    # Select DSCP marking method. | Default: static
    dscp_marking_method: Literal["multi-stage", "static"]
    # Exceed bandwidth used for DSCP/VLAN CoS multi-stage marking. | Default: 0 | Min: 0 | Max: 80000000
    exceed_bandwidth: int
    # DSCP mark for traffic in guaranteed-bandwidth and exceed-ban
    exceed_dscp: str
    # DSCP mark for traffic in exceed-bandwidth and maximum-bandwi
    maximum_dscp: str
    # Enable/disable VLAN CoS marking. | Default: disable
    cos_marking: Literal["enable", "disable"]
    # Select VLAN CoS marking method. | Default: static
    cos_marking_method: Literal["multi-stage", "static"]
    # VLAN CoS mark.
    cos: str
    # VLAN CoS mark for traffic in
    exceed_cos: str
    # VLAN CoS mark for traffic in
    maximum_cos: str
    # Per-packet size overhead used in rate computations. | Default: 0 | Min: 0 | Max: 100
    overhead: int
    # Class ID for traffic in guaranteed-bandwidth and maximum-ban | Default: 0 | Min: 0 | Max: 4294967295
    exceed_class_id: int
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> TrafficShaperPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class TrafficShaper:
    """
    Configure shared traffic shaper.
    
    Path: firewall/shaper/traffic_shaper
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
    ) -> TrafficShaperResponse: ...
    
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
    ) -> TrafficShaperResponse: ...
    
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
    ) -> list[TrafficShaperResponse]: ...
    
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
    ) -> TrafficShaperObject: ...
    
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
    ) -> TrafficShaperObject: ...
    
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
    ) -> list[TrafficShaperObject]: ...
    
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
    ) -> TrafficShaperResponse: ...
    
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
    ) -> TrafficShaperResponse: ...
    
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
    ) -> list[TrafficShaperResponse]: ...
    
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
    ) -> TrafficShaperObject | list[TrafficShaperObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficShaperObject: ...
    
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficShaperObject: ...
    
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
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
    ) -> TrafficShaperObject: ...
    
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
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
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

class TrafficShaperDictMode:
    """TrafficShaper endpoint for dict response mode (default for this client).
    
    By default returns TrafficShaperResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return TrafficShaperObject.
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
    ) -> TrafficShaperObject: ...
    
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
    ) -> list[TrafficShaperObject]: ...
    
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
    ) -> TrafficShaperResponse: ...
    
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
    ) -> list[TrafficShaperResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficShaperObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficShaperObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
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
    ) -> TrafficShaperObject: ...
    
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
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
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


class TrafficShaperObjectMode:
    """TrafficShaper endpoint for object response mode (default for this client).
    
    By default returns TrafficShaperObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return TrafficShaperResponse (TypedDict).
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
    ) -> TrafficShaperResponse: ...
    
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
    ) -> list[TrafficShaperResponse]: ...
    
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
    ) -> TrafficShaperObject: ...
    
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
    ) -> list[TrafficShaperObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficShaperObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> TrafficShaperObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> TrafficShaperObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> TrafficShaperObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
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
    ) -> TrafficShaperObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> TrafficShaperObject: ...
    
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
        payload_dict: TrafficShaperPayload | None = ...,
        name: str | None = ...,
        guaranteed_bandwidth: int | None = ...,
        maximum_bandwidth: int | None = ...,
        bandwidth_unit: Literal["kbps", "mbps", "gbps"] | None = ...,
        priority: Literal["low", "medium", "high"] | None = ...,
        per_policy: Literal["disable", "enable"] | None = ...,
        diffserv: Literal["enable", "disable"] | None = ...,
        diffservcode: str | None = ...,
        dscp_marking_method: Literal["multi-stage", "static"] | None = ...,
        exceed_bandwidth: int | None = ...,
        exceed_dscp: str | None = ...,
        maximum_dscp: str | None = ...,
        cos_marking: Literal["enable", "disable"] | None = ...,
        cos_marking_method: Literal["multi-stage", "static"] | None = ...,
        cos: str | None = ...,
        exceed_cos: str | None = ...,
        maximum_cos: str | None = ...,
        overhead: int | None = ...,
        exceed_class_id: int | None = ...,
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
    "TrafficShaper",
    "TrafficShaperDictMode",
    "TrafficShaperObjectMode",
    "TrafficShaperPayload",
    "TrafficShaperObject",
]