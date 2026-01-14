from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class OcspServerPayload(TypedDict, total=False):
    """
    Type hints for vpn/certificate/ocsp_server payload fields.
    
    OCSP server configuration.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.vpn.certificate.ca.CaEndpoint` (via: cert, secondary-cert)
        - :class:`~.vpn.certificate.remote.RemoteEndpoint` (via: cert, secondary-cert)

    **Usage:**
        payload: OcspServerPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # OCSP server entry name. | MaxLen: 35
    url: str  # OCSP server URL. | MaxLen: 127
    cert: str  # OCSP server certificate. | MaxLen: 127
    secondary_url: str  # Secondary OCSP server URL. | MaxLen: 127
    secondary_cert: str  # Secondary OCSP server certificate. | MaxLen: 127
    unavail_action: Literal["revoke", "ignore"]  # Action when server is unavailable | Default: revoke
    source_ip: str  # Source IP address for dynamic AIA and OCSP queries | MaxLen: 63

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class OcspServerResponse(TypedDict):
    """
    Type hints for vpn/certificate/ocsp_server API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # OCSP server entry name. | MaxLen: 35
    url: str  # OCSP server URL. | MaxLen: 127
    cert: str  # OCSP server certificate. | MaxLen: 127
    secondary_url: str  # Secondary OCSP server URL. | MaxLen: 127
    secondary_cert: str  # Secondary OCSP server certificate. | MaxLen: 127
    unavail_action: Literal["revoke", "ignore"]  # Action when server is unavailable | Default: revoke
    source_ip: str  # Source IP address for dynamic AIA and OCSP queries | MaxLen: 63


@final
class OcspServerObject:
    """Typed FortiObject for vpn/certificate/ocsp_server with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # OCSP server entry name. | MaxLen: 35
    name: str
    # OCSP server URL. | MaxLen: 127
    url: str
    # OCSP server certificate. | MaxLen: 127
    cert: str
    # Secondary OCSP server URL. | MaxLen: 127
    secondary_url: str
    # Secondary OCSP server certificate. | MaxLen: 127
    secondary_cert: str
    # Action when server is unavailable | Default: revoke
    unavail_action: Literal["revoke", "ignore"]
    # Source IP address for dynamic AIA and OCSP queries. | MaxLen: 63
    source_ip: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> OcspServerPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class OcspServer:
    """
    OCSP server configuration.
    
    Path: vpn/certificate/ocsp_server
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
    ) -> OcspServerResponse: ...
    
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
    ) -> OcspServerResponse: ...
    
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
    ) -> list[OcspServerResponse]: ...
    
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
    ) -> OcspServerObject: ...
    
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
    ) -> OcspServerObject: ...
    
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
    ) -> list[OcspServerObject]: ...
    
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
    ) -> OcspServerResponse: ...
    
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
    ) -> OcspServerResponse: ...
    
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
    ) -> list[OcspServerResponse]: ...
    
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
    ) -> OcspServerObject | list[OcspServerObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OcspServerObject: ...
    
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OcspServerObject: ...
    
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
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
    ) -> OcspServerObject: ...
    
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
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
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

class OcspServerDictMode:
    """OcspServer endpoint for dict response mode (default for this client).
    
    By default returns OcspServerResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return OcspServerObject.
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
    ) -> OcspServerObject: ...
    
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
    ) -> list[OcspServerObject]: ...
    
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
    ) -> OcspServerResponse: ...
    
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
    ) -> list[OcspServerResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OcspServerObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OcspServerObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
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
    ) -> OcspServerObject: ...
    
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
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
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


class OcspServerObjectMode:
    """OcspServer endpoint for object response mode (default for this client).
    
    By default returns OcspServerObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return OcspServerResponse (TypedDict).
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
    ) -> OcspServerResponse: ...
    
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
    ) -> list[OcspServerResponse]: ...
    
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
    ) -> OcspServerObject: ...
    
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
    ) -> list[OcspServerObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OcspServerObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> OcspServerObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> OcspServerObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> OcspServerObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
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
    ) -> OcspServerObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> OcspServerObject: ...
    
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
        payload_dict: OcspServerPayload | None = ...,
        name: str | None = ...,
        url: str | None = ...,
        cert: str | None = ...,
        secondary_url: str | None = ...,
        secondary_cert: str | None = ...,
        unavail_action: Literal["revoke", "ignore"] | None = ...,
        source_ip: str | None = ...,
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
    "OcspServer",
    "OcspServerDictMode",
    "OcspServerObjectMode",
    "OcspServerPayload",
    "OcspServerObject",
]