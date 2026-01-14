from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class DataplanPayload(TypedDict, total=False):
    """
    Type hints for extension_controller/dataplan payload fields.
    
    FortiExtender dataplan configuration.
    
    **Usage:**
        payload: DataplanPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # FortiExtender data plan name. | MaxLen: 31
    modem_id: Literal["modem1", "modem2", "all"]  # Dataplan's modem specifics, if any. | Default: all
    type: Literal["carrier", "slot", "iccid", "generic"]  # Type preferences configuration. | Default: generic
    slot: Literal["sim1", "sim2"]  # SIM slot configuration.
    iccid: str  # ICCID configuration. | MaxLen: 31
    carrier: str  # Carrier configuration. | MaxLen: 31
    apn: str  # APN configuration. | MaxLen: 63
    auth_type: Literal["none", "pap", "chap"]  # Authentication type. | Default: none
    username: str  # Username. | MaxLen: 127
    password: str  # Password. | MaxLen: 64
    pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"]  # PDN type. | Default: ipv4-only
    signal_threshold: int  # Signal threshold. Specify the range between 50 - 1 | Default: 100 | Min: 50 | Max: 100
    signal_period: int  # Signal period (600 to 18000 seconds). | Default: 3600 | Min: 600 | Max: 18000
    capacity: int  # Capacity in MB (0 - 102400000). | Default: 0 | Min: 0 | Max: 102400000
    monthly_fee: int  # Monthly fee of dataplan | Default: 0 | Min: 0 | Max: 1000000
    billing_date: int  # Billing day of the month (1 - 31). | Default: 1 | Min: 1 | Max: 31
    overage: Literal["disable", "enable"]  # Enable/disable dataplan overage detection. | Default: disable
    preferred_subnet: int  # Preferred subnet mask (0 - 32). | Default: 0 | Min: 0 | Max: 32
    private_network: Literal["disable", "enable"]  # Enable/disable dataplan private network support. | Default: disable

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class DataplanResponse(TypedDict):
    """
    Type hints for extension_controller/dataplan API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # FortiExtender data plan name. | MaxLen: 31
    modem_id: Literal["modem1", "modem2", "all"]  # Dataplan's modem specifics, if any. | Default: all
    type: Literal["carrier", "slot", "iccid", "generic"]  # Type preferences configuration. | Default: generic
    slot: Literal["sim1", "sim2"]  # SIM slot configuration.
    iccid: str  # ICCID configuration. | MaxLen: 31
    carrier: str  # Carrier configuration. | MaxLen: 31
    apn: str  # APN configuration. | MaxLen: 63
    auth_type: Literal["none", "pap", "chap"]  # Authentication type. | Default: none
    username: str  # Username. | MaxLen: 127
    password: str  # Password. | MaxLen: 64
    pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"]  # PDN type. | Default: ipv4-only
    signal_threshold: int  # Signal threshold. Specify the range between 50 - 1 | Default: 100 | Min: 50 | Max: 100
    signal_period: int  # Signal period (600 to 18000 seconds). | Default: 3600 | Min: 600 | Max: 18000
    capacity: int  # Capacity in MB (0 - 102400000). | Default: 0 | Min: 0 | Max: 102400000
    monthly_fee: int  # Monthly fee of dataplan | Default: 0 | Min: 0 | Max: 1000000
    billing_date: int  # Billing day of the month (1 - 31). | Default: 1 | Min: 1 | Max: 31
    overage: Literal["disable", "enable"]  # Enable/disable dataplan overage detection. | Default: disable
    preferred_subnet: int  # Preferred subnet mask (0 - 32). | Default: 0 | Min: 0 | Max: 32
    private_network: Literal["disable", "enable"]  # Enable/disable dataplan private network support. | Default: disable


@final
class DataplanObject:
    """Typed FortiObject for extension_controller/dataplan with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # FortiExtender data plan name. | MaxLen: 31
    name: str
    # Dataplan's modem specifics, if any. | Default: all
    modem_id: Literal["modem1", "modem2", "all"]
    # Type preferences configuration. | Default: generic
    type: Literal["carrier", "slot", "iccid", "generic"]
    # SIM slot configuration.
    slot: Literal["sim1", "sim2"]
    # ICCID configuration. | MaxLen: 31
    iccid: str
    # Carrier configuration. | MaxLen: 31
    carrier: str
    # APN configuration. | MaxLen: 63
    apn: str
    # Authentication type. | Default: none
    auth_type: Literal["none", "pap", "chap"]
    # Username. | MaxLen: 127
    username: str
    # Password. | MaxLen: 64
    password: str
    # PDN type. | Default: ipv4-only
    pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"]
    # Signal threshold. Specify the range between 50 - 100, where | Default: 100 | Min: 50 | Max: 100
    signal_threshold: int
    # Signal period (600 to 18000 seconds). | Default: 3600 | Min: 600 | Max: 18000
    signal_period: int
    # Capacity in MB (0 - 102400000). | Default: 0 | Min: 0 | Max: 102400000
    capacity: int
    # Monthly fee of dataplan (0 - 100000, in local currency). | Default: 0 | Min: 0 | Max: 1000000
    monthly_fee: int
    # Billing day of the month (1 - 31). | Default: 1 | Min: 1 | Max: 31
    billing_date: int
    # Enable/disable dataplan overage detection. | Default: disable
    overage: Literal["disable", "enable"]
    # Preferred subnet mask (0 - 32). | Default: 0 | Min: 0 | Max: 32
    preferred_subnet: int
    # Enable/disable dataplan private network support. | Default: disable
    private_network: Literal["disable", "enable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> DataplanPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Dataplan:
    """
    FortiExtender dataplan configuration.
    
    Path: extension_controller/dataplan
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
    ) -> DataplanResponse: ...
    
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
    ) -> DataplanResponse: ...
    
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
    ) -> list[DataplanResponse]: ...
    
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
    ) -> DataplanObject: ...
    
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
    ) -> DataplanObject: ...
    
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
    ) -> list[DataplanObject]: ...
    
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
    ) -> DataplanResponse: ...
    
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
    ) -> DataplanResponse: ...
    
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
    ) -> list[DataplanResponse]: ...
    
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
    ) -> DataplanObject | list[DataplanObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DataplanObject: ...
    
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DataplanObject: ...
    
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
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
    ) -> DataplanObject: ...
    
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
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
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

class DataplanDictMode:
    """Dataplan endpoint for dict response mode (default for this client).
    
    By default returns DataplanResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return DataplanObject.
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
    ) -> DataplanObject: ...
    
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
    ) -> list[DataplanObject]: ...
    
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
    ) -> DataplanResponse: ...
    
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
    ) -> list[DataplanResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DataplanObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DataplanObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
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
    ) -> DataplanObject: ...
    
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
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
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


class DataplanObjectMode:
    """Dataplan endpoint for object response mode (default for this client).
    
    By default returns DataplanObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return DataplanResponse (TypedDict).
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
    ) -> DataplanResponse: ...
    
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
    ) -> list[DataplanResponse]: ...
    
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
    ) -> DataplanObject: ...
    
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
    ) -> list[DataplanObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DataplanObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> DataplanObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DataplanObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> DataplanObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
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
    ) -> DataplanObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> DataplanObject: ...
    
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
        payload_dict: DataplanPayload | None = ...,
        name: str | None = ...,
        modem_id: Literal["modem1", "modem2", "all"] | None = ...,
        type: Literal["carrier", "slot", "iccid", "generic"] | None = ...,
        slot: Literal["sim1", "sim2"] | None = ...,
        iccid: str | None = ...,
        carrier: str | None = ...,
        apn: str | None = ...,
        auth_type: Literal["none", "pap", "chap"] | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        pdn: Literal["ipv4-only", "ipv6-only", "ipv4-ipv6"] | None = ...,
        signal_threshold: int | None = ...,
        signal_period: int | None = ...,
        capacity: int | None = ...,
        monthly_fee: int | None = ...,
        billing_date: int | None = ...,
        overage: Literal["disable", "enable"] | None = ...,
        preferred_subnet: int | None = ...,
        private_network: Literal["disable", "enable"] | None = ...,
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
    "Dataplan",
    "DataplanDictMode",
    "DataplanObjectMode",
    "DataplanPayload",
    "DataplanObject",
]