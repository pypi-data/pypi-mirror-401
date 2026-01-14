from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class GroupPayload(TypedDict, total=False):
    """
    Type hints for user/group payload fields.
    
    Configure user groups.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.sms-server.SmsServerEndpoint` (via: sms-custom-server)

    **Usage:**
        payload: GroupPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Group name. | MaxLen: 35
    id: int  # Group ID. | Default: 0 | Min: 0 | Max: 4294967295
    group_type: Literal["firewall", "fsso-service", "rsso", "guest"]  # Set the group to be for firewall authentication, F | Default: firewall
    authtimeout: int  # Authentication timeout in minutes for this user gr | Default: 0 | Min: 0 | Max: 43200
    auth_concurrent_override: Literal["enable", "disable"]  # Enable/disable overriding the global number of con | Default: disable
    auth_concurrent_value: int  # Maximum number of concurrent authenticated connect | Default: 0 | Min: 0 | Max: 100
    http_digest_realm: str  # Realm attribute for MD5-digest authentication. | MaxLen: 35
    sso_attribute_value: str  # RADIUS attribute value. | MaxLen: 511
    member: list[dict[str, Any]]  # Names of users, peers, LDAP severs, RADIUS servers
    match: list[dict[str, Any]]  # Group matches.
    user_id: Literal["email", "auto-generate", "specify"]  # Guest user ID type. | Default: email
    password: Literal["auto-generate", "specify", "disable"]  # Guest user password type. | Default: auto-generate
    user_name: Literal["disable", "enable"]  # Enable/disable the guest user name entry. | Default: disable
    sponsor: Literal["optional", "mandatory", "disabled"]  # Set the action for the sponsor guest user field. | Default: optional
    company: Literal["optional", "mandatory", "disabled"]  # Set the action for the company guest user field. | Default: optional
    email: Literal["disable", "enable"]  # Enable/disable the guest user email address field. | Default: enable
    mobile_phone: Literal["disable", "enable"]  # Enable/disable the guest user mobile phone number | Default: disable
    sms_server: Literal["fortiguard", "custom"]  # Send SMS through FortiGuard or other external serv | Default: fortiguard
    sms_custom_server: str  # SMS server. | MaxLen: 35
    expire_type: Literal["immediately", "first-successful-login"]  # Determine when the expiration countdown begins. | Default: immediately
    expire: int  # Time in seconds before guest user accounts expire | Default: 14400 | Min: 1 | Max: 31536000
    max_accounts: int  # Maximum number of guest accounts that can be creat | Default: 0 | Min: 0 | Max: 500
    multiple_guest_add: Literal["disable", "enable"]  # Enable/disable addition of multiple guests. | Default: disable
    guest: list[dict[str, Any]]  # Guest User.

# Nested TypedDicts for table field children (dict mode)

class GroupMemberItem(TypedDict):
    """Type hints for member table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Group member name. | MaxLen: 511


class GroupMatchItem(TypedDict):
    """Type hints for match table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # ID. | Default: 0 | Min: 0 | Max: 4294967295
    server_name: str  # Name of remote auth server. | MaxLen: 35
    group_name: str  # Name of matching user or group on remote authentic | MaxLen: 511


class GroupGuestItem(TypedDict):
    """Type hints for guest table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: int  # Guest ID. | Default: 0 | Min: 0 | Max: 4294967295
    user_id: str  # Guest ID. | MaxLen: 64
    name: str  # Guest name. | MaxLen: 64
    password: str  # Guest password. | MaxLen: 128
    mobile_phone: str  # Mobile phone. | MaxLen: 35
    sponsor: str  # Set the action for the sponsor guest user field. | MaxLen: 35
    company: str  # Set the action for the company guest user field. | MaxLen: 35
    email: str  # Email. | MaxLen: 64
    expiration: str  # Expire time.
    comment: str  # Comment. | MaxLen: 255


# Nested classes for table field children (object mode)

@final
class GroupMemberObject:
    """Typed object for member table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Group member name. | MaxLen: 511
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
class GroupMatchObject:
    """Typed object for match table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # Name of remote auth server. | MaxLen: 35
    server_name: str
    # Name of matching user or group on remote authentication serv | MaxLen: 511
    group_name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class GroupGuestObject:
    """Typed object for guest table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Guest ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # Guest ID. | MaxLen: 64
    user_id: str
    # Guest name. | MaxLen: 64
    name: str
    # Guest password. | MaxLen: 128
    password: str
    # Mobile phone. | MaxLen: 35
    mobile_phone: str
    # Set the action for the sponsor guest user field. | MaxLen: 35
    sponsor: str
    # Set the action for the company guest user field. | MaxLen: 35
    company: str
    # Email. | MaxLen: 64
    email: str
    # Expire time.
    expiration: str
    # Comment. | MaxLen: 255
    comment: str
    
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
    Type hints for user/group API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Group name. | MaxLen: 35
    id: int  # Group ID. | Default: 0 | Min: 0 | Max: 4294967295
    group_type: Literal["firewall", "fsso-service", "rsso", "guest"]  # Set the group to be for firewall authentication, F | Default: firewall
    authtimeout: int  # Authentication timeout in minutes for this user gr | Default: 0 | Min: 0 | Max: 43200
    auth_concurrent_override: Literal["enable", "disable"]  # Enable/disable overriding the global number of con | Default: disable
    auth_concurrent_value: int  # Maximum number of concurrent authenticated connect | Default: 0 | Min: 0 | Max: 100
    http_digest_realm: str  # Realm attribute for MD5-digest authentication. | MaxLen: 35
    sso_attribute_value: str  # RADIUS attribute value. | MaxLen: 511
    member: list[GroupMemberItem]  # Names of users, peers, LDAP severs, RADIUS servers
    match: list[GroupMatchItem]  # Group matches.
    user_id: Literal["email", "auto-generate", "specify"]  # Guest user ID type. | Default: email
    password: Literal["auto-generate", "specify", "disable"]  # Guest user password type. | Default: auto-generate
    user_name: Literal["disable", "enable"]  # Enable/disable the guest user name entry. | Default: disable
    sponsor: Literal["optional", "mandatory", "disabled"]  # Set the action for the sponsor guest user field. | Default: optional
    company: Literal["optional", "mandatory", "disabled"]  # Set the action for the company guest user field. | Default: optional
    email: Literal["disable", "enable"]  # Enable/disable the guest user email address field. | Default: enable
    mobile_phone: Literal["disable", "enable"]  # Enable/disable the guest user mobile phone number | Default: disable
    sms_server: Literal["fortiguard", "custom"]  # Send SMS through FortiGuard or other external serv | Default: fortiguard
    sms_custom_server: str  # SMS server. | MaxLen: 35
    expire_type: Literal["immediately", "first-successful-login"]  # Determine when the expiration countdown begins. | Default: immediately
    expire: int  # Time in seconds before guest user accounts expire | Default: 14400 | Min: 1 | Max: 31536000
    max_accounts: int  # Maximum number of guest accounts that can be creat | Default: 0 | Min: 0 | Max: 500
    multiple_guest_add: Literal["disable", "enable"]  # Enable/disable addition of multiple guests. | Default: disable
    guest: list[GroupGuestItem]  # Guest User.


@final
class GroupObject:
    """Typed FortiObject for user/group with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Group name. | MaxLen: 35
    name: str
    # Group ID. | Default: 0 | Min: 0 | Max: 4294967295
    id: int
    # Set the group to be for firewall authentication, FSSO, RSSO, | Default: firewall
    group_type: Literal["firewall", "fsso-service", "rsso", "guest"]
    # Authentication timeout in minutes for this user group. 0 to | Default: 0 | Min: 0 | Max: 43200
    authtimeout: int
    # Enable/disable overriding the global number of concurrent au | Default: disable
    auth_concurrent_override: Literal["enable", "disable"]
    # Maximum number of concurrent authenticated connections per u | Default: 0 | Min: 0 | Max: 100
    auth_concurrent_value: int
    # Realm attribute for MD5-digest authentication. | MaxLen: 35
    http_digest_realm: str
    # RADIUS attribute value. | MaxLen: 511
    sso_attribute_value: str
    # Names of users, peers, LDAP severs, RADIUS servers or extern
    member: list[GroupMemberObject]
    # Group matches.
    match: list[GroupMatchObject]
    # Guest user ID type. | Default: email
    user_id: Literal["email", "auto-generate", "specify"]
    # Guest user password type. | Default: auto-generate
    password: Literal["auto-generate", "specify", "disable"]
    # Enable/disable the guest user name entry. | Default: disable
    user_name: Literal["disable", "enable"]
    # Set the action for the sponsor guest user field. | Default: optional
    sponsor: Literal["optional", "mandatory", "disabled"]
    # Set the action for the company guest user field. | Default: optional
    company: Literal["optional", "mandatory", "disabled"]
    # Enable/disable the guest user email address field. | Default: enable
    email: Literal["disable", "enable"]
    # Enable/disable the guest user mobile phone number field. | Default: disable
    mobile_phone: Literal["disable", "enable"]
    # Send SMS through FortiGuard or other external server. | Default: fortiguard
    sms_server: Literal["fortiguard", "custom"]
    # SMS server. | MaxLen: 35
    sms_custom_server: str
    # Determine when the expiration countdown begins. | Default: immediately
    expire_type: Literal["immediately", "first-successful-login"]
    # Time in seconds before guest user accounts expire | Default: 14400 | Min: 1 | Max: 31536000
    expire: int
    # Maximum number of guest accounts that can be created for thi | Default: 0 | Min: 0 | Max: 500
    max_accounts: int
    # Enable/disable addition of multiple guests. | Default: disable
    multiple_guest_add: Literal["disable", "enable"]
    # Guest User.
    guest: list[GroupGuestObject]
    
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
    Configure user groups.
    
    Path: user/group
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> GroupObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> GroupObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: GroupPayload | None = ...,
        name: str | None = ...,
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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
        id: int | None = ...,
        group_type: Literal["firewall", "fsso-service", "rsso", "guest"] | None = ...,
        authtimeout: int | None = ...,
        auth_concurrent_override: Literal["enable", "disable"] | None = ...,
        auth_concurrent_value: int | None = ...,
        http_digest_realm: str | None = ...,
        sso_attribute_value: str | None = ...,
        member: str | list[str] | list[dict[str, Any]] | None = ...,
        match: str | list[str] | list[dict[str, Any]] | None = ...,
        user_id: Literal["email", "auto-generate", "specify"] | None = ...,
        password: Literal["auto-generate", "specify", "disable"] | None = ...,
        user_name: Literal["disable", "enable"] | None = ...,
        sponsor: Literal["optional", "mandatory", "disabled"] | None = ...,
        company: Literal["optional", "mandatory", "disabled"] | None = ...,
        email: Literal["disable", "enable"] | None = ...,
        mobile_phone: Literal["disable", "enable"] | None = ...,
        sms_server: Literal["fortiguard", "custom"] | None = ...,
        sms_custom_server: str | None = ...,
        expire_type: Literal["immediately", "first-successful-login"] | None = ...,
        expire: int | None = ...,
        max_accounts: int | None = ...,
        multiple_guest_add: Literal["disable", "enable"] | None = ...,
        guest: str | list[str] | list[dict[str, Any]] | None = ...,
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