from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class AddrgrpPayload(TypedDict, total=False):
    """
    Type hints for firewall/addrgrp payload fields.
    
    Configure IPv4 address groups.
    
    **Usage:**
        payload: AddrgrpPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Address group name. | MaxLen: 79
    type: Literal["default", "folder"]  # Address group type. | Default: default
    category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"]  # Address group category. | Default: default
    allow_routing: Literal["enable", "disable"]  # Enable/disable use of this group in routing config | Default: disable
    member: list[dict[str, Any]]  # Address objects contained within the group.
    comment: str  # Comment. | MaxLen: 255
    uuid: str  # Universally Unique Identifier | Default: 00000000-0000-0000-0000-000000000000
    exclude: Literal["enable", "disable"]  # Enable/disable address exclusion. | Default: disable
    exclude_member: list[dict[str, Any]]  # Address exclusion member.
    color: int  # Color of icon on the GUI. | Default: 0 | Min: 0 | Max: 32
    tagging: list[dict[str, Any]]  # Config object tagging.
    fabric_object: Literal["enable", "disable"]  # Security Fabric global object setting. | Default: disable

# Nested TypedDicts for table field children (dict mode)

class AddrgrpMemberItem(TypedDict):
    """Type hints for member table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Address name. | MaxLen: 79


class AddrgrpExcludememberItem(TypedDict):
    """Type hints for exclude-member table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Address name. | MaxLen: 79


class AddrgrpTaggingItem(TypedDict):
    """Type hints for tagging table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Tagging entry name. | MaxLen: 63
    category: str  # Tag category. | MaxLen: 63
    tags: str  # Tags.


# Nested classes for table field children (object mode)

@final
class AddrgrpMemberObject:
    """Typed object for member table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Address name. | MaxLen: 79
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
class AddrgrpExcludememberObject:
    """Typed object for exclude-member table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Address name. | MaxLen: 79
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
class AddrgrpTaggingObject:
    """Typed object for tagging table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Tagging entry name. | MaxLen: 63
    name: str
    # Tag category. | MaxLen: 63
    category: str
    # Tags.
    tags: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class AddrgrpResponse(TypedDict):
    """
    Type hints for firewall/addrgrp API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Address group name. | MaxLen: 79
    type: Literal["default", "folder"]  # Address group type. | Default: default
    category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"]  # Address group category. | Default: default
    allow_routing: Literal["enable", "disable"]  # Enable/disable use of this group in routing config | Default: disable
    member: list[AddrgrpMemberItem]  # Address objects contained within the group.
    comment: str  # Comment. | MaxLen: 255
    uuid: str  # Universally Unique Identifier | Default: 00000000-0000-0000-0000-000000000000
    exclude: Literal["enable", "disable"]  # Enable/disable address exclusion. | Default: disable
    exclude_member: list[AddrgrpExcludememberItem]  # Address exclusion member.
    color: int  # Color of icon on the GUI. | Default: 0 | Min: 0 | Max: 32
    tagging: list[AddrgrpTaggingItem]  # Config object tagging.
    fabric_object: Literal["enable", "disable"]  # Security Fabric global object setting. | Default: disable


@final
class AddrgrpObject:
    """Typed FortiObject for firewall/addrgrp with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Address group name. | MaxLen: 79
    name: str
    # Address group type. | Default: default
    type: Literal["default", "folder"]
    # Address group category. | Default: default
    category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"]
    # Enable/disable use of this group in routing configurations. | Default: disable
    allow_routing: Literal["enable", "disable"]
    # Address objects contained within the group.
    member: list[AddrgrpMemberObject]
    # Comment. | MaxLen: 255
    comment: str
    # Universally Unique Identifier | Default: 00000000-0000-0000-0000-000000000000
    uuid: str
    # Enable/disable address exclusion. | Default: disable
    exclude: Literal["enable", "disable"]
    # Address exclusion member.
    exclude_member: list[AddrgrpExcludememberObject]
    # Color of icon on the GUI. | Default: 0 | Min: 0 | Max: 32
    color: int
    # Config object tagging.
    tagging: list[AddrgrpTaggingObject]
    # Security Fabric global object setting. | Default: disable
    fabric_object: Literal["enable", "disable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> AddrgrpPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Addrgrp:
    """
    Configure IPv4 address groups.
    
    Path: firewall/addrgrp
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
    ) -> AddrgrpResponse: ...
    
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
    ) -> AddrgrpResponse: ...
    
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
    ) -> list[AddrgrpResponse]: ...
    
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
    ) -> AddrgrpObject: ...
    
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
    ) -> AddrgrpObject: ...
    
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
    ) -> list[AddrgrpObject]: ...
    
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
    ) -> AddrgrpResponse: ...
    
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
    ) -> AddrgrpResponse: ...
    
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
    ) -> list[AddrgrpResponse]: ...
    
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
    ) -> AddrgrpObject | list[AddrgrpObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AddrgrpObject: ...
    
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AddrgrpObject: ...
    
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
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
    ) -> AddrgrpObject: ...
    
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
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
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

class AddrgrpDictMode:
    """Addrgrp endpoint for dict response mode (default for this client).
    
    By default returns AddrgrpResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return AddrgrpObject.
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
    ) -> AddrgrpObject: ...
    
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
    ) -> list[AddrgrpObject]: ...
    
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
    ) -> AddrgrpResponse: ...
    
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
    ) -> list[AddrgrpResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AddrgrpObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AddrgrpObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
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
    ) -> AddrgrpObject: ...
    
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
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
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


class AddrgrpObjectMode:
    """Addrgrp endpoint for object response mode (default for this client).
    
    By default returns AddrgrpObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return AddrgrpResponse (TypedDict).
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
    ) -> AddrgrpResponse: ...
    
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
    ) -> list[AddrgrpResponse]: ...
    
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
    ) -> AddrgrpObject: ...
    
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
    ) -> list[AddrgrpObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AddrgrpObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AddrgrpObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AddrgrpObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AddrgrpObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
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
    ) -> AddrgrpObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AddrgrpObject: ...
    
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
        payload_dict: AddrgrpPayload | None = ...,
        name: str | None = ...,
        type: Literal["default", "folder"] | None = ...,
        category: Literal["default", "ztna-ems-tag", "ztna-geo-tag"] | None = ...,
        allow_routing: Literal["enable", "disable"] | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        comment: str | None = ...,
        uuid: str | None = ...,
        exclude: Literal["enable", "disable"] | None = ...,
        exclude_member: str | list[str] | list[dict[str, Any]] | None = ...,
        color: int | None = ...,
        tagging: str | list[str] | list[dict[str, Any]] | None = ...,
        fabric_object: Literal["enable", "disable"] | None = ...,
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
    "Addrgrp",
    "AddrgrpDictMode",
    "AddrgrpObjectMode",
    "AddrgrpPayload",
    "AddrgrpObject",
]