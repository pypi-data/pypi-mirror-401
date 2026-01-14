from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class ManualkeyPayload(TypedDict, total=False):
    """
    Type hints for vpn/ipsec/manualkey payload fields.
    
    Configure IPsec manual keys.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: interface)

    **Usage:**
        payload: ManualkeyPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # IPsec tunnel name. | MaxLen: 35
    interface: str  # Name of the physical, aggregate, or VLAN interface | MaxLen: 15
    remote_gw: str  # Peer gateway. | Default: 0.0.0.0
    local_gw: str  # Local gateway. | Default: 0.0.0.0
    authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"]  # Authentication algorithm. Must be the same for bot | Default: null
    encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"]  # Encryption algorithm. Must be the same for both en | Default: null
    authkey: str  # Hexadecimal authentication key in 16-digit
    enckey: str  # Hexadecimal encryption key in 16-digit (8-byte) se
    localspi: str  # Local SPI, a hexadecimal 8-digit (4-byte) tag. Dis
    remotespi: str  # Remote SPI, a hexadecimal 8-digit (4-byte) tag. Di
    npu_offload: Literal["enable", "disable"]  # Enable/disable NPU offloading. | Default: enable

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class ManualkeyResponse(TypedDict):
    """
    Type hints for vpn/ipsec/manualkey API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # IPsec tunnel name. | MaxLen: 35
    interface: str  # Name of the physical, aggregate, or VLAN interface | MaxLen: 15
    remote_gw: str  # Peer gateway. | Default: 0.0.0.0
    local_gw: str  # Local gateway. | Default: 0.0.0.0
    authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"]  # Authentication algorithm. Must be the same for bot | Default: null
    encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"]  # Encryption algorithm. Must be the same for both en | Default: null
    authkey: str  # Hexadecimal authentication key in 16-digit
    enckey: str  # Hexadecimal encryption key in 16-digit (8-byte) se
    localspi: str  # Local SPI, a hexadecimal 8-digit (4-byte) tag. Dis
    remotespi: str  # Remote SPI, a hexadecimal 8-digit (4-byte) tag. Di
    npu_offload: Literal["enable", "disable"]  # Enable/disable NPU offloading. | Default: enable


@final
class ManualkeyObject:
    """Typed FortiObject for vpn/ipsec/manualkey with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # IPsec tunnel name. | MaxLen: 35
    name: str
    # Name of the physical, aggregate, or VLAN interface. | MaxLen: 15
    interface: str
    # Peer gateway. | Default: 0.0.0.0
    remote_gw: str
    # Local gateway. | Default: 0.0.0.0
    local_gw: str
    # Authentication algorithm. Must be the same for both ends of | Default: null
    authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"]
    # Encryption algorithm. Must be the same for both ends of the | Default: null
    encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"]
    # Hexadecimal authentication key in 16-digit (8-byte) segments
    authkey: str
    # Hexadecimal encryption key in 16-digit (8-byte) segments sep
    enckey: str
    # Local SPI, a hexadecimal 8-digit (4-byte) tag. Discerns betw
    localspi: str
    # Remote SPI, a hexadecimal 8-digit (4-byte) tag. Discerns bet
    remotespi: str
    # Enable/disable NPU offloading. | Default: enable
    npu_offload: Literal["enable", "disable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> ManualkeyPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Manualkey:
    """
    Configure IPsec manual keys.
    
    Path: vpn/ipsec/manualkey
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
    ) -> ManualkeyResponse: ...
    
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
    ) -> ManualkeyResponse: ...
    
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
    ) -> list[ManualkeyResponse]: ...
    
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
    ) -> ManualkeyObject: ...
    
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
    ) -> ManualkeyObject: ...
    
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
    ) -> list[ManualkeyObject]: ...
    
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
    ) -> ManualkeyResponse: ...
    
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
    ) -> ManualkeyResponse: ...
    
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
    ) -> list[ManualkeyResponse]: ...
    
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
    ) -> ManualkeyObject | list[ManualkeyObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ManualkeyObject: ...
    
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ManualkeyObject: ...
    
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
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
    ) -> ManualkeyObject: ...
    
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
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
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

class ManualkeyDictMode:
    """Manualkey endpoint for dict response mode (default for this client).
    
    By default returns ManualkeyResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return ManualkeyObject.
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
    ) -> ManualkeyObject: ...
    
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
    ) -> list[ManualkeyObject]: ...
    
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
    ) -> ManualkeyResponse: ...
    
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
    ) -> list[ManualkeyResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ManualkeyObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ManualkeyObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
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
    ) -> ManualkeyObject: ...
    
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
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
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


class ManualkeyObjectMode:
    """Manualkey endpoint for object response mode (default for this client).
    
    By default returns ManualkeyObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return ManualkeyResponse (TypedDict).
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
    ) -> ManualkeyResponse: ...
    
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
    ) -> list[ManualkeyResponse]: ...
    
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
    ) -> ManualkeyObject: ...
    
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
    ) -> list[ManualkeyObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ManualkeyObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ManualkeyObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> ManualkeyObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ManualkeyObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
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
    ) -> ManualkeyObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> ManualkeyObject: ...
    
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
        payload_dict: ManualkeyPayload | None = ...,
        name: str | None = ...,
        interface: str | None = ...,
        remote_gw: str | None = ...,
        local_gw: str | None = ...,
        authentication: Literal["null", "md5", "sha1", "sha256", "sha384", "sha512"] | None = ...,
        encryption: Literal["null", "des", "3des", "aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "seed"] | None = ...,
        authkey: str | None = ...,
        enckey: str | None = ...,
        localspi: str | None = ...,
        remotespi: str | None = ...,
        npu_offload: Literal["enable", "disable"] | None = ...,
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
    "Manualkey",
    "ManualkeyDictMode",
    "ManualkeyObjectMode",
    "ManualkeyPayload",
    "ManualkeyObject",
]