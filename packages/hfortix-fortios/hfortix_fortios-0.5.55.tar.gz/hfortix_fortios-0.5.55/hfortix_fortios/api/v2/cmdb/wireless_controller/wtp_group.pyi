from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class WtpGroupPayload(TypedDict, total=False):
    """
    Type hints for wireless_controller/wtp_group payload fields.
    
    Configure WTP groups.
    
    **Usage:**
        payload: WtpGroupPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # WTP group name. | MaxLen: 35
    platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"]  # FortiAP models to define the WTP group platform ty
    ble_major_id: int  # Override BLE Major ID. | Default: 0 | Min: 0 | Max: 65535
    wtps: list[dict[str, Any]]  # WTP list.

# Nested TypedDicts for table field children (dict mode)

class WtpGroupWtpsItem(TypedDict):
    """Type hints for wtps table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    wtp_id: str  # WTP ID. | MaxLen: 35


# Nested classes for table field children (object mode)

@final
class WtpGroupWtpsObject:
    """Typed object for wtps table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # WTP ID. | MaxLen: 35
    wtp_id: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class WtpGroupResponse(TypedDict):
    """
    Type hints for wireless_controller/wtp_group API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # WTP group name. | MaxLen: 35
    platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"]  # FortiAP models to define the WTP group platform ty
    ble_major_id: int  # Override BLE Major ID. | Default: 0 | Min: 0 | Max: 65535
    wtps: list[WtpGroupWtpsItem]  # WTP list.


@final
class WtpGroupObject:
    """Typed FortiObject for wireless_controller/wtp_group with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # WTP group name. | MaxLen: 35
    name: str
    # FortiAP models to define the WTP group platform type.
    platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"]
    # Override BLE Major ID. | Default: 0 | Min: 0 | Max: 65535
    ble_major_id: int
    # WTP list.
    wtps: list[WtpGroupWtpsObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> WtpGroupPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class WtpGroup:
    """
    Configure WTP groups.
    
    Path: wireless_controller/wtp_group
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
    ) -> WtpGroupResponse: ...
    
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
    ) -> WtpGroupResponse: ...
    
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
    ) -> list[WtpGroupResponse]: ...
    
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
    ) -> WtpGroupObject: ...
    
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
    ) -> WtpGroupObject: ...
    
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
    ) -> list[WtpGroupObject]: ...
    
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
    ) -> WtpGroupResponse: ...
    
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
    ) -> WtpGroupResponse: ...
    
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
    ) -> list[WtpGroupResponse]: ...
    
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
    ) -> WtpGroupObject | list[WtpGroupObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WtpGroupObject: ...
    
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WtpGroupObject: ...
    
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> WtpGroupObject: ...
    
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
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
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

class WtpGroupDictMode:
    """WtpGroup endpoint for dict response mode (default for this client).
    
    By default returns WtpGroupResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return WtpGroupObject.
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
    ) -> WtpGroupObject: ...
    
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
    ) -> list[WtpGroupObject]: ...
    
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
    ) -> WtpGroupResponse: ...
    
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
    ) -> list[WtpGroupResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WtpGroupObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WtpGroupObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> WtpGroupObject: ...
    
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
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
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


class WtpGroupObjectMode:
    """WtpGroup endpoint for object response mode (default for this client).
    
    By default returns WtpGroupObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return WtpGroupResponse (TypedDict).
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
    ) -> WtpGroupResponse: ...
    
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
    ) -> list[WtpGroupResponse]: ...
    
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
    ) -> WtpGroupObject: ...
    
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
    ) -> list[WtpGroupObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WtpGroupObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> WtpGroupObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WtpGroupObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> WtpGroupObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> WtpGroupObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> WtpGroupObject: ...
    
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
        payload_dict: WtpGroupPayload | None = ...,
        name: str | None = ...,
        platform_type: Literal["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"] | None = ...,
        ble_major_id: int | None = ...,
        wtps: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "WtpGroup",
    "WtpGroupDictMode",
    "WtpGroupObjectMode",
    "WtpGroupPayload",
    "WtpGroupObject",
]