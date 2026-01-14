from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class GroupPayload(TypedDict, total=False):
    """
    Type hints for application/group payload fields.
    
    Configure firewall application groups.
    
    **Usage:**
        payload: GroupPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Application group name. | MaxLen: 63
    comment: str  # Comments. | MaxLen: 255
    type: Literal["application", "filter"]  # Application group type. | Default: application
    application: list[dict[str, Any]]  # Application ID list.
    category: list[dict[str, Any]]  # Application category ID list.
    risk: list[dict[str, Any]]  # Risk, or impact, of allowing traffic from this app
    protocols: list[dict[str, Any]]  # Application protocol filter. | Default: all
    vendor: list[dict[str, Any]]  # Application vendor filter. | Default: all
    technology: list[dict[str, Any]]  # Application technology filter. | Default: all
    behavior: list[dict[str, Any]]  # Application behavior filter. | Default: all
    popularity: Literal["1", "2", "3", "4", "5"]  # Application popularity filter | Default: 1 2 3 4 5

# Nested TypedDicts for table field children (dict mode)

class GroupApplicationItem(TypedDict):
    """Type hints for application table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Application IDs. | Default: 0 | Min: 0 | Max: 4294967295


class GroupCategoryItem(TypedDict):
    """Type hints for category table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Category IDs. | Default: 0 | Min: 0 | Max: 4294967295


class GroupRiskItem(TypedDict):
    """Type hints for risk table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    level: int  # Risk, or impact, of allowing traffic from this app | Default: 0 | Min: 0 | Max: 4294967295


# Nested classes for table field children (object mode)

@final
class GroupApplicationObject:
    """Typed object for application table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Application IDs. | Default: 0 | Min: 0 | Max: 4294967295
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
class GroupCategoryObject:
    """Typed object for category table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Category IDs. | Default: 0 | Min: 0 | Max: 4294967295
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
class GroupRiskObject:
    """Typed object for risk table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Risk, or impact, of allowing traffic from this application t | Default: 0 | Min: 0 | Max: 4294967295
    level: int
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class GroupResponse(TypedDict):
    """
    Type hints for application/group API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Application group name. | MaxLen: 63
    comment: str  # Comments. | MaxLen: 255
    type: Literal["application", "filter"]  # Application group type. | Default: application
    application: list[GroupApplicationItem]  # Application ID list.
    category: list[GroupCategoryItem]  # Application category ID list.
    risk: list[GroupRiskItem]  # Risk, or impact, of allowing traffic from this app
    protocols: list[dict[str, Any]]  # Application protocol filter. | Default: all
    vendor: list[dict[str, Any]]  # Application vendor filter. | Default: all
    technology: list[dict[str, Any]]  # Application technology filter. | Default: all
    behavior: list[dict[str, Any]]  # Application behavior filter. | Default: all
    popularity: Literal["1", "2", "3", "4", "5"]  # Application popularity filter | Default: 1 2 3 4 5


@final
class GroupObject:
    """Typed FortiObject for application/group with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Application group name. | MaxLen: 63
    name: str
    # Comments. | MaxLen: 255
    comment: str
    # Application group type. | Default: application
    type: Literal["application", "filter"]
    # Application ID list.
    application: list[GroupApplicationObject]
    # Application category ID list.
    category: list[GroupCategoryObject]
    # Risk, or impact, of allowing traffic from this application t
    risk: list[GroupRiskObject]
    # Application protocol filter. | Default: all
    protocols: list[dict[str, Any]]
    # Application vendor filter. | Default: all
    vendor: list[dict[str, Any]]
    # Application technology filter. | Default: all
    technology: list[dict[str, Any]]
    # Application behavior filter. | Default: all
    behavior: list[dict[str, Any]]
    # Application popularity filter | Default: 1 2 3 4 5
    popularity: Literal["1", "2", "3", "4", "5"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> GroupPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Group:
    """
    Configure firewall application groups.
    
    Path: application/group
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
    ) -> GroupResponse: ...
    
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
    ) -> GroupResponse: ...
    
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
    ) -> list[GroupResponse]: ...
    
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
    ) -> GroupObject: ...
    
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
    ) -> GroupObject: ...
    
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
    ) -> list[GroupObject]: ...
    
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
    ) -> GroupResponse: ...
    
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
    ) -> GroupResponse: ...
    
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
    ) -> list[GroupResponse]: ...
    
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
    ) -> GroupObject | list[GroupObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> GroupObject: ...
    
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> GroupObject: ...
    
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
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
    ) -> GroupObject: ...
    
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
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
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

class GroupDictMode:
    """Group endpoint for dict response mode (default for this client).
    
    By default returns GroupResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return GroupObject.
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
    ) -> GroupObject: ...
    
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
    ) -> list[GroupObject]: ...
    
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
    ) -> GroupResponse: ...
    
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
    ) -> list[GroupResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> GroupObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> GroupObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
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
    ) -> GroupObject: ...
    
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
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
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


class GroupObjectMode:
    """Group endpoint for object response mode (default for this client).
    
    By default returns GroupObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return GroupResponse (TypedDict).
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
    ) -> GroupResponse: ...
    
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
    ) -> list[GroupResponse]: ...
    
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
    ) -> GroupObject: ...
    
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
    ) -> list[GroupObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> GroupObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> GroupObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> GroupObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> GroupObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
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
    ) -> GroupObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> GroupObject: ...
    
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
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        type: Literal["application", "filter"] | None = ...,
        application: str | list[str] | list[dict[str, Any]] | None = ...,
        category: str | list[str] | list[dict[str, Any]] | None = ...,
        risk: str | list[str] | list[dict[str, Any]] | None = ...,
        protocols: str | list[str] | None = ...,
        vendor: str | list[str] | None = ...,
        technology: str | list[str] | None = ...,
        behavior: str | list[str] | None = ...,
        popularity: Literal["1", "2", "3", "4", "5"] | list[str] | None = ...,
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
    "Group",
    "GroupDictMode",
    "GroupObjectMode",
    "GroupPayload",
    "GroupObject",
]