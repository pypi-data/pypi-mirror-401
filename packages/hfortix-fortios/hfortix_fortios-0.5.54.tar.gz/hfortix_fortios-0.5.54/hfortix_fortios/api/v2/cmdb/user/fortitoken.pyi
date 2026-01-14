from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class FortitokenPayload(TypedDict, total=False):
    """
    Type hints for user/fortitoken payload fields.
    
    Configure FortiToken.
    
    **Usage:**
        payload: FortitokenPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    serial_number: str  # Serial number. | MaxLen: 16
    status: Literal["active", "lock"]  # Status. | Default: active
    comments: str  # Comment. | MaxLen: 255
    license: str  # Mobile token license. | MaxLen: 31
    activation_code: str  # Mobile token user activation-code. | MaxLen: 32
    activation_expire: int  # Mobile token user activation-code expire time. | Default: 0 | Min: 0 | Max: 4294967295
    reg_id: str  # Device Reg ID. | MaxLen: 256
    os_ver: str  # Device Mobile Version. | MaxLen: 15

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class FortitokenResponse(TypedDict):
    """
    Type hints for user/fortitoken API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    serial_number: str  # Serial number. | MaxLen: 16
    status: Literal["active", "lock"]  # Status. | Default: active
    comments: str  # Comment. | MaxLen: 255
    license: str  # Mobile token license. | MaxLen: 31
    activation_code: str  # Mobile token user activation-code. | MaxLen: 32
    activation_expire: int  # Mobile token user activation-code expire time. | Default: 0 | Min: 0 | Max: 4294967295
    reg_id: str  # Device Reg ID. | MaxLen: 256
    os_ver: str  # Device Mobile Version. | MaxLen: 15


@final
class FortitokenObject:
    """Typed FortiObject for user/fortitoken with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Serial number. | MaxLen: 16
    serial_number: str
    # Status. | Default: active
    status: Literal["active", "lock"]
    # Comment. | MaxLen: 255
    comments: str
    # Mobile token license. | MaxLen: 31
    license: str
    # Mobile token user activation-code. | MaxLen: 32
    activation_code: str
    # Mobile token user activation-code expire time. | Default: 0 | Min: 0 | Max: 4294967295
    activation_expire: int
    # Device Reg ID. | MaxLen: 256
    reg_id: str
    # Device Mobile Version. | MaxLen: 15
    os_ver: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> FortitokenPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Fortitoken:
    """
    Configure FortiToken.
    
    Path: user/fortitoken
    Category: cmdb
    Primary Key: serial-number
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
        serial_number: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> FortitokenResponse: ...
    
    # Default mode: mkey as keyword arg -> returns typed dict
    @overload
    def get(
        self,
        *,
        serial_number: str,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> FortitokenResponse: ...
    
    # Default mode: no mkey -> returns list of typed dicts
    @overload
    def get(
        self,
        serial_number: None = None,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[FortitokenResponse]: ...
    
    # ================================================================
    # EXPLICIT response_mode="object" OVERLOADS
    # ================================================================
    
    # Object mode: mkey as positional arg -> returns single object
    @overload
    def get(
        self,
        serial_number: str,
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
    ) -> FortitokenObject: ...
    
    # Object mode: mkey as keyword arg -> returns single object
    @overload
    def get(
        self,
        *,
        serial_number: str,
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
    ) -> FortitokenObject: ...
    
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
    ) -> list[FortitokenObject]: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def get(
        self,
        serial_number: str | None = ...,
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
        serial_number: str,
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
    ) -> FortitokenResponse: ...
    
    # Dict mode with mkey provided as keyword arg (single dict)
    @overload
    def get(
        self,
        *,
        serial_number: str,
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
    ) -> FortitokenResponse: ...
    
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
    ) -> list[FortitokenResponse]: ...
    
    # Fallback overload for all other cases
    @overload
    def get(
        self,
        serial_number: str | None = ...,
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
        serial_number: str | None = ...,
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
    ) -> FortitokenObject | list[FortitokenObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE overloads
    @overload
    def delete(
        self,
        serial_number: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    @overload
    def delete(
        self,
        serial_number: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def delete(
        self,
        serial_number: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def delete(
        self,
        serial_number: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def delete(
        self,
        serial_number: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
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

class FortitokenDictMode:
    """Fortitoken endpoint for dict response mode (default for this client).
    
    By default returns FortitokenResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return FortitokenObject.
    """
    
    # raw_json=True returns RawAPIResponse regardless of response_mode
    @overload
    def get(
        self,
        serial_number: str | None = ...,
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
        serial_number: str,
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
    ) -> FortitokenObject: ...
    
    # Object mode override without mkey (list)
    @overload
    def get(
        self,
        serial_number: None = ...,
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
    ) -> list[FortitokenObject]: ...
    
    # Dict mode with mkey (single item) - default
    @overload
    def get(
        self,
        serial_number: str,
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
    ) -> FortitokenResponse: ...
    
    # Dict mode without mkey (list) - default
    @overload
    def get(
        self,
        serial_number: None = ...,
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
    ) -> list[FortitokenResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Object mode override
    @overload
    def delete(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    # DELETE - Default overload (returns MutationResponse)
    @overload
    def delete(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Dict mode (default for DictMode class)
    def delete(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
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


class FortitokenObjectMode:
    """Fortitoken endpoint for object response mode (default for this client).
    
    By default returns FortitokenObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return FortitokenResponse (TypedDict).
    """
    
    # raw_json=True returns RawAPIResponse for GET
    @overload
    def get(
        self,
        serial_number: str | None = ...,
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
        serial_number: str,
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
    ) -> FortitokenResponse: ...
    
    # Dict mode override without mkey (list)
    @overload
    def get(
        self,
        serial_number: None = ...,
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
    ) -> list[FortitokenResponse]: ...
    
    # Object mode with mkey (single item) - default
    @overload
    def get(
        self,
        serial_number: str,
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
    ) -> FortitokenObject: ...
    
    # Object mode without mkey (list) - default
    @overload
    def get(
        self,
        serial_number: None = ...,
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
    ) -> list[FortitokenObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Dict mode override
    @overload
    def delete(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Object mode override (requires explicit response_mode="object")
    @overload
    def delete(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortitokenObject: ...
    
    # DELETE - Default for ObjectMode (returns MutationResponse like DictMode)
    def delete(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        serial_number: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: FortitokenPayload | None = ...,
        serial_number: str | None = ...,
        status: Literal["active", "lock"] | None = ...,
        comments: str | None = ...,
        license: str | None = ...,
        activation_code: str | None = ...,
        activation_expire: int | None = ...,
        reg_id: str | None = ...,
        os_ver: str | None = ...,
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
    "Fortitoken",
    "FortitokenDictMode",
    "FortitokenObjectMode",
    "FortitokenPayload",
    "FortitokenObject",
]