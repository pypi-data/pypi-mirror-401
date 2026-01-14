from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class AutomationStitchPayload(TypedDict, total=False):
    """
    Type hints for system/automation_stitch payload fields.
    
    Automation stitches.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.automation-trigger.AutomationTriggerEndpoint` (via: trigger)

    **Usage:**
        payload: AutomationStitchPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Name. | MaxLen: 35
    description: str  # Description. | MaxLen: 255
    status: Literal["enable", "disable"]  # Enable/disable this stitch. | Default: enable
    trigger: str  # Trigger name. | MaxLen: 35
    condition: list[dict[str, Any]]  # Automation conditions.
    condition_logic: Literal["and", "or"]  # Apply AND/OR logic to the specified automation con | Default: and
    actions: list[dict[str, Any]]  # Configure stitch actions.
    destination: list[dict[str, Any]]  # Serial number/HA group-name of destination devices

# Nested TypedDicts for table field children (dict mode)

class AutomationStitchConditionItem(TypedDict):
    """Type hints for condition table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Condition name. | MaxLen: 79


class AutomationStitchActionsItem(TypedDict):
    """Type hints for actions table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Entry ID. | Default: 0 | Min: 0 | Max: 4294967295
    action: str  # Action name. | MaxLen: 64
    delay: int  # Delay before execution (in seconds). | Default: 0 | Min: 0 | Max: 3600
    required: Literal["enable", "disable"]  # Required in action chain. | Default: disable


class AutomationStitchDestinationItem(TypedDict):
    """Type hints for destination table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Destination name. | MaxLen: 79


# Nested classes for table field children (object mode)

@final
class AutomationStitchConditionObject:
    """Typed object for condition table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Condition name. | MaxLen: 79
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
class AutomationStitchActionsObject:
    """Typed object for actions table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Entry ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # Action name. | MaxLen: 64
    action: str
    # Delay before execution (in seconds). | Default: 0 | Min: 0 | Max: 3600
    delay: int
    # Required in action chain. | Default: disable
    required: Literal["enable", "disable"]
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class AutomationStitchDestinationObject:
    """Typed object for destination table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Destination name. | MaxLen: 79
    name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class AutomationStitchResponse(TypedDict):
    """
    Type hints for system/automation_stitch API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Name. | MaxLen: 35
    description: str  # Description. | MaxLen: 255
    status: Literal["enable", "disable"]  # Enable/disable this stitch. | Default: enable
    trigger: str  # Trigger name. | MaxLen: 35
    condition: list[AutomationStitchConditionItem]  # Automation conditions.
    condition_logic: Literal["and", "or"]  # Apply AND/OR logic to the specified automation con | Default: and
    actions: list[AutomationStitchActionsItem]  # Configure stitch actions.
    destination: list[AutomationStitchDestinationItem]  # Serial number/HA group-name of destination devices


@final
class AutomationStitchObject:
    """Typed FortiObject for system/automation_stitch with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Name. | MaxLen: 35
    name: str
    # Description. | MaxLen: 255
    description: str
    # Enable/disable this stitch. | Default: enable
    status: Literal["enable", "disable"]
    # Trigger name. | MaxLen: 35
    trigger: str
    # Automation conditions.
    condition: list[AutomationStitchConditionObject]
    # Apply AND/OR logic to the specified automation conditions. | Default: and
    condition_logic: Literal["and", "or"]
    # Configure stitch actions.
    actions: list[AutomationStitchActionsObject]
    # Serial number/HA group-name of destination devices.
    destination: list[AutomationStitchDestinationObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> AutomationStitchPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class AutomationStitch:
    """
    Automation stitches.
    
    Path: system/automation_stitch
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
    ) -> AutomationStitchResponse: ...
    
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
    ) -> AutomationStitchResponse: ...
    
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
    ) -> list[AutomationStitchResponse]: ...
    
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
    ) -> AutomationStitchObject: ...
    
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
    ) -> AutomationStitchObject: ...
    
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
    ) -> list[AutomationStitchObject]: ...
    
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
    ) -> AutomationStitchResponse: ...
    
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
    ) -> AutomationStitchResponse: ...
    
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
    ) -> list[AutomationStitchResponse]: ...
    
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
    ) -> AutomationStitchObject | list[AutomationStitchObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationStitchObject: ...
    
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationStitchObject: ...
    
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> AutomationStitchObject: ...
    
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
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
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

class AutomationStitchDictMode:
    """AutomationStitch endpoint for dict response mode (default for this client).
    
    By default returns AutomationStitchResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return AutomationStitchObject.
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
    ) -> AutomationStitchObject: ...
    
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
    ) -> list[AutomationStitchObject]: ...
    
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
    ) -> AutomationStitchResponse: ...
    
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
    ) -> list[AutomationStitchResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationStitchObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationStitchObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> AutomationStitchObject: ...
    
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
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
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


class AutomationStitchObjectMode:
    """AutomationStitch endpoint for object response mode (default for this client).
    
    By default returns AutomationStitchObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return AutomationStitchResponse (TypedDict).
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
    ) -> AutomationStitchResponse: ...
    
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
    ) -> list[AutomationStitchResponse]: ...
    
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
    ) -> AutomationStitchObject: ...
    
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
    ) -> list[AutomationStitchObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationStitchObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AutomationStitchObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AutomationStitchObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AutomationStitchObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
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
    ) -> AutomationStitchObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AutomationStitchObject: ...
    
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
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[dict[str, Any]] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[dict[str, Any]] | None = ...,
        destination: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "AutomationStitch",
    "AutomationStitchDictMode",
    "AutomationStitchObjectMode",
    "AutomationStitchPayload",
    "AutomationStitchObject",
]