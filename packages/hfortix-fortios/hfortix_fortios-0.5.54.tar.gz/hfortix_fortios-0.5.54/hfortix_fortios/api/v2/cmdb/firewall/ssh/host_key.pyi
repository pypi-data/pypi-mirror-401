from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class HostKeyPayload(TypedDict, total=False):
    """
    Type hints for firewall/ssh/host_key payload fields.
    
    SSH proxy host public keys.
    
    **Usage:**
        payload: HostKeyPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # SSH public key name. | MaxLen: 35
    status: Literal["trusted", "revoked"]  # Set the trust status of the public key. | Default: trusted
    type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"]  # Set the type of the public key. | Default: RSA
    nid: Literal["256", "384", "521"]  # Set the nid of the ECDSA key. | Default: 256
    usage: Literal["transparent-proxy", "access-proxy"]  # Usage for this public key. | Default: transparent-proxy
    ip: str  # IP address of the SSH server. | Default: 0.0.0.0
    port: int  # Port of the SSH server. | Default: 22 | Min: 0 | Max: 4294967295
    hostname: str  # Hostname of the SSH server to match SSH certificat | MaxLen: 255
    public_key: str  # SSH public key. | MaxLen: 32768

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class HostKeyResponse(TypedDict):
    """
    Type hints for firewall/ssh/host_key API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # SSH public key name. | MaxLen: 35
    status: Literal["trusted", "revoked"]  # Set the trust status of the public key. | Default: trusted
    type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"]  # Set the type of the public key. | Default: RSA
    nid: Literal["256", "384", "521"]  # Set the nid of the ECDSA key. | Default: 256
    usage: Literal["transparent-proxy", "access-proxy"]  # Usage for this public key. | Default: transparent-proxy
    ip: str  # IP address of the SSH server. | Default: 0.0.0.0
    port: int  # Port of the SSH server. | Default: 22 | Min: 0 | Max: 4294967295
    hostname: str  # Hostname of the SSH server to match SSH certificat | MaxLen: 255
    public_key: str  # SSH public key. | MaxLen: 32768


@final
class HostKeyObject:
    """Typed FortiObject for firewall/ssh/host_key with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # SSH public key name. | MaxLen: 35
    name: str
    # Set the trust status of the public key. | Default: trusted
    status: Literal["trusted", "revoked"]
    # Set the type of the public key. | Default: RSA
    type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"]
    # Set the nid of the ECDSA key. | Default: 256
    nid: Literal["256", "384", "521"]
    # Usage for this public key. | Default: transparent-proxy
    usage: Literal["transparent-proxy", "access-proxy"]
    # IP address of the SSH server. | Default: 0.0.0.0
    ip: str
    # Port of the SSH server. | Default: 22 | Min: 0 | Max: 4294967295
    port: int
    # Hostname of the SSH server to match SSH certificate principa | MaxLen: 255
    hostname: str
    # SSH public key. | MaxLen: 32768
    public_key: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> HostKeyPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class HostKey:
    """
    SSH proxy host public keys.
    
    Path: firewall/ssh/host_key
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
    ) -> HostKeyResponse: ...
    
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
    ) -> HostKeyResponse: ...
    
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
    ) -> list[HostKeyResponse]: ...
    
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
    ) -> HostKeyObject: ...
    
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
    ) -> HostKeyObject: ...
    
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
    ) -> list[HostKeyObject]: ...
    
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
    ) -> HostKeyResponse: ...
    
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
    ) -> HostKeyResponse: ...
    
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
    ) -> list[HostKeyResponse]: ...
    
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
    ) -> HostKeyObject | list[HostKeyObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HostKeyObject: ...
    
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HostKeyObject: ...
    
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
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
    ) -> HostKeyObject: ...
    
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
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
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

class HostKeyDictMode:
    """HostKey endpoint for dict response mode (default for this client).
    
    By default returns HostKeyResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return HostKeyObject.
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
    ) -> HostKeyObject: ...
    
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
    ) -> list[HostKeyObject]: ...
    
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
    ) -> HostKeyResponse: ...
    
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
    ) -> list[HostKeyResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HostKeyObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HostKeyObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
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
    ) -> HostKeyObject: ...
    
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
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
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


class HostKeyObjectMode:
    """HostKey endpoint for object response mode (default for this client).
    
    By default returns HostKeyObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return HostKeyResponse (TypedDict).
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
    ) -> HostKeyResponse: ...
    
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
    ) -> list[HostKeyResponse]: ...
    
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
    ) -> HostKeyObject: ...
    
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
    ) -> list[HostKeyObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HostKeyObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> HostKeyObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HostKeyObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> HostKeyObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
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
    ) -> HostKeyObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> HostKeyObject: ...
    
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
        payload_dict: HostKeyPayload | None = ...,
        name: str | None = ...,
        status: Literal["trusted", "revoked"] | None = ...,
        type: Literal["RSA", "DSA", "ECDSA", "ED25519", "RSA-CA", "DSA-CA", "ECDSA-CA", "ED25519-CA"] | None = ...,
        nid: Literal["256", "384", "521"] | None = ...,
        usage: Literal["transparent-proxy", "access-proxy"] | None = ...,
        ip: str | None = ...,
        port: int | None = ...,
        hostname: str | None = ...,
        public_key: str | None = ...,
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
    "HostKey",
    "HostKeyDictMode",
    "HostKeyObjectMode",
    "HostKeyPayload",
    "HostKeyObject",
]