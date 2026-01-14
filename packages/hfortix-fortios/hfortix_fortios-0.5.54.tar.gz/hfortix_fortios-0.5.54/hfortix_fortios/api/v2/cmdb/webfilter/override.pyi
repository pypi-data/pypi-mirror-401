from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class OverridePayload(TypedDict, total=False):
    """
    Type hints for webfilter/override payload fields.
    
    Configure FortiGuard Web Filter administrative overrides.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.user.group.GroupEndpoint` (via: user-group)
        - :class:`~.webfilter.profile.ProfileEndpoint` (via: new-profile, old-profile)

    **Usage:**
        payload: OverridePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    id: int  # Override rule ID. | Default: 0 | Min: 0 | Max: 4294967295
    status: Literal["enable", "disable"]  # Enable/disable override rule. | Default: disable
    scope: Literal["user", "user-group", "ip", "ip6"]  # Override either the specific user, user group, IPv | Default: user
    ip: str  # IPv4 address which the override applies. | Default: 0.0.0.0
    user: str  # Name of the user which the override applies. | MaxLen: 64
    user_group: str  # Specify the user group for which the override appl | MaxLen: 63
    old_profile: str  # Name of the web filter profile which the override | MaxLen: 47
    new_profile: str  # Name of the new web filter profile used by the ove | MaxLen: 47
    ip6: str  # IPv6 address which the override applies. | Default: ::
    expires: str  # Override expiration date and time, from 5 minutes | Default: 1970/01/01 00:00:00
    initiator: str  # Initiating user of override (read-only setting). | MaxLen: 64

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class OverrideResponse(TypedDict):
    """
    Type hints for webfilter/override API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    id: int  # Override rule ID. | Default: 0 | Min: 0 | Max: 4294967295
    status: Literal["enable", "disable"]  # Enable/disable override rule. | Default: disable
    scope: Literal["user", "user-group", "ip", "ip6"]  # Override either the specific user, user group, IPv | Default: user
    ip: str  # IPv4 address which the override applies. | Default: 0.0.0.0
    user: str  # Name of the user which the override applies. | MaxLen: 64
    user_group: str  # Specify the user group for which the override appl | MaxLen: 63
    old_profile: str  # Name of the web filter profile which the override | MaxLen: 47
    new_profile: str  # Name of the new web filter profile used by the ove | MaxLen: 47
    ip6: str  # IPv6 address which the override applies. | Default: ::
    expires: str  # Override expiration date and time, from 5 minutes | Default: 1970/01/01 00:00:00
    initiator: str  # Initiating user of override (read-only setting). | MaxLen: 64


@final
class OverrideObject:
    """Typed FortiObject for webfilter/override with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Override rule ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # Enable/disable override rule. | Default: disable
    status: Literal["enable", "disable"]
    # Override either the specific user, user group, IPv4 address, | Default: user
    scope: Literal["user", "user-group", "ip", "ip6"]
    # IPv4 address which the override applies. | Default: 0.0.0.0
    ip: str
    # Name of the user which the override applies. | MaxLen: 64
    user: str
    # Specify the user group for which the override applies. | MaxLen: 63
    user_group: str
    # Name of the web filter profile which the override applies. | MaxLen: 47
    old_profile: str
    # Name of the new web filter profile used by the override. | MaxLen: 47
    new_profile: str
    # IPv6 address which the override applies. | Default: ::
    ip6: str
    # Override expiration date and time, from 5 minutes to 365 fro | Default: 1970/01/01 00:00:00
    expires: str
    # Initiating user of override (read-only setting). | MaxLen: 64
    initiator: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> OverridePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Override:
    """
    Configure FortiGuard Web Filter administrative overrides.
    
    Path: webfilter/override
    Category: cmdb
    Primary Key: id
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
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> OverrideResponse: ...
    
    # Default mode: mkey as keyword arg -> returns typed dict
    @overload
    def get(
        self,
        *,
        id: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> OverrideResponse: ...
    
    # Default mode: no mkey -> returns list of typed dicts
    @overload
    def get(
        self,
        id: None = None,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[OverrideResponse]: ...
    
    # ================================================================
    # EXPLICIT response_mode="object" OVERLOADS
    # ================================================================
    
    # Object mode: mkey as positional arg -> returns single object
    @overload
    def get(
        self,
        id: int,
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
    ) -> OverrideObject: ...
    
    # Object mode: mkey as keyword arg -> returns single object
    @overload
    def get(
        self,
        *,
        id: int,
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
    ) -> OverrideObject: ...
    
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
    ) -> list[OverrideObject]: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int,
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
    ) -> OverrideResponse: ...
    
    # Dict mode with mkey provided as keyword arg (single dict)
    @overload
    def get(
        self,
        *,
        id: int,
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
    ) -> OverrideResponse: ...
    
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
    ) -> list[OverrideResponse]: ...
    
    # Fallback overload for all other cases
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int | None = ...,
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
    ) -> OverrideObject | list[OverrideObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE overloads
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
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

class OverrideDictMode:
    """Override endpoint for dict response mode (default for this client).
    
    By default returns OverrideResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return OverrideObject.
    """
    
    # raw_json=True returns RawAPIResponse regardless of response_mode
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int,
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
    ) -> OverrideObject: ...
    
    # Object mode override without mkey (list)
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[OverrideObject]: ...
    
    # Dict mode with mkey (single item) - default
    @overload
    def get(
        self,
        id: int,
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
    ) -> OverrideResponse: ...
    
    # Dict mode without mkey (list) - default
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[OverrideResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Object mode override
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    # DELETE - Default overload (returns MutationResponse)
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Dict mode (default for DictMode class)
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
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


class OverrideObjectMode:
    """Override endpoint for object response mode (default for this client).
    
    By default returns OverrideObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return OverrideResponse (TypedDict).
    """
    
    # raw_json=True returns RawAPIResponse for GET
    @overload
    def get(
        self,
        id: int | None = ...,
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
        id: int,
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
    ) -> OverrideResponse: ...
    
    # Dict mode override without mkey (list)
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[OverrideResponse]: ...
    
    # Object mode with mkey (single item) - default
    @overload
    def get(
        self,
        id: int,
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
    ) -> OverrideObject: ...
    
    # Object mode without mkey (list) - default
    @overload
    def get(
        self,
        id: None = ...,
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
    ) -> list[OverrideObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Dict mode override
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Object mode override (requires explicit response_mode="object")
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> OverrideObject: ...
    
    # DELETE - Default for ObjectMode (returns MutationResponse like DictMode)
    def delete(
        self,
        id: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: OverridePayload | None = ...,
        id: int | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        scope: Literal["user", "user-group", "ip", "ip6"] | None = ...,
        ip: str | None = ...,
        user: str | None = ...,
        user_group: str | None = ...,
        old_profile: str | None = ...,
        new_profile: str | None = ...,
        ip6: str | None = ...,
        expires: str | None = ...,
        initiator: str | None = ...,
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
    "Override",
    "OverrideDictMode",
    "OverrideObjectMode",
    "OverridePayload",
    "OverrideObject",
]