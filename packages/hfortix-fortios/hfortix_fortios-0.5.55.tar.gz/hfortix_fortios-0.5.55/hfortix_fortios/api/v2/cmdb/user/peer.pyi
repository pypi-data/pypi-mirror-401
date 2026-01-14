from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class PeerPayload(TypedDict, total=False):
    """
    Type hints for user/peer payload fields.
    
    Configure peer users.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.user.ldap.LdapEndpoint` (via: mfa-server)
        - :class:`~.user.radius.RadiusEndpoint` (via: mfa-server)
        - :class:`~.vpn.certificate.ca.CaEndpoint` (via: ca)
        - :class:`~.vpn.certificate.ocsp-server.OcspServerEndpoint` (via: ocsp-override-server)

    **Usage:**
        payload: PeerPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Peer name. | MaxLen: 35
    mandatory_ca_verify: Literal["enable", "disable"]  # Determine what happens to the peer if the CA certi | Default: enable
    ca: str  # Name of the CA certificate. | MaxLen: 127
    subject: str  # Peer certificate name constraints. | MaxLen: 255
    cn: str  # Peer certificate common name. | MaxLen: 255
    cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"]  # Peer certificate common name type. | Default: string
    mfa_mode: Literal["none", "password", "subject-identity"]  # MFA mode for remote peer authentication/authorizat | Default: none
    mfa_server: str  # Name of a remote authenticator. Performs client ac | MaxLen: 35
    mfa_username: str  # Unified username for remote authentication. | MaxLen: 35
    mfa_password: str  # Unified password for remote authentication. This f | MaxLen: 128
    ocsp_override_server: str  # Online Certificate Status Protocol (OCSP) server f | MaxLen: 35
    two_factor: Literal["enable", "disable"]  # Enable/disable two-factor authentication, applying | Default: disable
    passwd: str  # Peer's password used for two-factor authentication | MaxLen: 128

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class PeerResponse(TypedDict):
    """
    Type hints for user/peer API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Peer name. | MaxLen: 35
    mandatory_ca_verify: Literal["enable", "disable"]  # Determine what happens to the peer if the CA certi | Default: enable
    ca: str  # Name of the CA certificate. | MaxLen: 127
    subject: str  # Peer certificate name constraints. | MaxLen: 255
    cn: str  # Peer certificate common name. | MaxLen: 255
    cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"]  # Peer certificate common name type. | Default: string
    mfa_mode: Literal["none", "password", "subject-identity"]  # MFA mode for remote peer authentication/authorizat | Default: none
    mfa_server: str  # Name of a remote authenticator. Performs client ac | MaxLen: 35
    mfa_username: str  # Unified username for remote authentication. | MaxLen: 35
    mfa_password: str  # Unified password for remote authentication. This f | MaxLen: 128
    ocsp_override_server: str  # Online Certificate Status Protocol (OCSP) server f | MaxLen: 35
    two_factor: Literal["enable", "disable"]  # Enable/disable two-factor authentication, applying | Default: disable
    passwd: str  # Peer's password used for two-factor authentication | MaxLen: 128


@final
class PeerObject:
    """Typed FortiObject for user/peer with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Peer name. | MaxLen: 35
    name: str
    # Determine what happens to the peer if the CA certificate is | Default: enable
    mandatory_ca_verify: Literal["enable", "disable"]
    # Name of the CA certificate. | MaxLen: 127
    ca: str
    # Peer certificate name constraints. | MaxLen: 255
    subject: str
    # Peer certificate common name. | MaxLen: 255
    cn: str
    # Peer certificate common name type. | Default: string
    cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"]
    # MFA mode for remote peer authentication/authorization. | Default: none
    mfa_mode: Literal["none", "password", "subject-identity"]
    # Name of a remote authenticator. Performs client access right | MaxLen: 35
    mfa_server: str
    # Unified username for remote authentication. | MaxLen: 35
    mfa_username: str
    # Unified password for remote authentication. This field may b | MaxLen: 128
    mfa_password: str
    # Online Certificate Status Protocol (OCSP) server for certifi | MaxLen: 35
    ocsp_override_server: str
    # Enable/disable two-factor authentication, applying certifica | Default: disable
    two_factor: Literal["enable", "disable"]
    # Peer's password used for two-factor authentication. | MaxLen: 128
    passwd: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> PeerPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Peer:
    """
    Configure peer users.
    
    Path: user/peer
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
    ) -> PeerResponse: ...
    
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
    ) -> PeerResponse: ...
    
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
    ) -> list[PeerResponse]: ...
    
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
    ) -> PeerObject: ...
    
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
    ) -> PeerObject: ...
    
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
    ) -> list[PeerObject]: ...
    
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
    ) -> PeerResponse: ...
    
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
    ) -> PeerResponse: ...
    
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
    ) -> list[PeerResponse]: ...
    
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
    ) -> PeerObject | list[PeerObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PeerObject: ...
    
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PeerObject: ...
    
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
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
    ) -> PeerObject: ...
    
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
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
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

class PeerDictMode:
    """Peer endpoint for dict response mode (default for this client).
    
    By default returns PeerResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return PeerObject.
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
    ) -> PeerObject: ...
    
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
    ) -> list[PeerObject]: ...
    
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
    ) -> PeerResponse: ...
    
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
    ) -> list[PeerResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PeerObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PeerObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
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
    ) -> PeerObject: ...
    
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
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
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


class PeerObjectMode:
    """Peer endpoint for object response mode (default for this client).
    
    By default returns PeerObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return PeerResponse (TypedDict).
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
    ) -> PeerResponse: ...
    
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
    ) -> list[PeerResponse]: ...
    
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
    ) -> PeerObject: ...
    
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
    ) -> list[PeerObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PeerObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> PeerObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> PeerObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> PeerObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
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
    ) -> PeerObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> PeerObject: ...
    
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
        payload_dict: PeerPayload | None = ...,
        name: str | None = ...,
        mandatory_ca_verify: Literal["enable", "disable"] | None = ...,
        ca: str | None = ...,
        subject: str | None = ...,
        cn: str | None = ...,
        cn_type: Literal["string", "email", "FQDN", "ipv4", "ipv6"] | None = ...,
        mfa_mode: Literal["none", "password", "subject-identity"] | None = ...,
        mfa_server: str | None = ...,
        mfa_username: str | None = ...,
        mfa_password: str | None = ...,
        ocsp_override_server: str | None = ...,
        two_factor: Literal["enable", "disable"] | None = ...,
        passwd: str | None = ...,
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
    "Peer",
    "PeerDictMode",
    "PeerObjectMode",
    "PeerPayload",
    "PeerObject",
]