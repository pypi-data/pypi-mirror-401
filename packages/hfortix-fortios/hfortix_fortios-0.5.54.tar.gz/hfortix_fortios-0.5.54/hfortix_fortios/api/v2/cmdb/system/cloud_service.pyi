from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class CloudServicePayload(TypedDict, total=False):
    """
    Type hints for system/cloud_service payload fields.
    
    Configure system cloud service.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.vdom.VdomEndpoint` (via: traffic-vdom)

    **Usage:**
        payload: CloudServicePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Name. | MaxLen: 35
    vendor: Literal["unknown", "google-cloud-kms"]  # Cloud service vendor. | Default: unknown
    traffic_vdom: str  # Vdom used to communicate with cloud service. | MaxLen: 31
    gck_service_account: str  # Service account | MaxLen: 285
    gck_private_key: str  # Service account private key in PEM format | MaxLen: 8191
    gck_keyid: str  # Key id, also referred as "kid". | MaxLen: 127
    gck_access_token_lifetime: int  # Lifetime of automatically generated access tokens | Default: 60 | Min: 1 | Max: 3600

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class CloudServiceResponse(TypedDict):
    """
    Type hints for system/cloud_service API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Name. | MaxLen: 35
    vendor: Literal["unknown", "google-cloud-kms"]  # Cloud service vendor. | Default: unknown
    traffic_vdom: str  # Vdom used to communicate with cloud service. | MaxLen: 31
    gck_service_account: str  # Service account | MaxLen: 285
    gck_private_key: str  # Service account private key in PEM format | MaxLen: 8191
    gck_keyid: str  # Key id, also referred as "kid". | MaxLen: 127
    gck_access_token_lifetime: int  # Lifetime of automatically generated access tokens | Default: 60 | Min: 1 | Max: 3600


@final
class CloudServiceObject:
    """Typed FortiObject for system/cloud_service with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Name. | MaxLen: 35
    name: str
    # Cloud service vendor. | Default: unknown
    vendor: Literal["unknown", "google-cloud-kms"]
    # Vdom used to communicate with cloud service. | MaxLen: 31
    traffic_vdom: str
    # Service account (e.g. "account-id@sampledomain.com"). | MaxLen: 285
    gck_service_account: str
    # Service account private key in PEM format | MaxLen: 8191
    gck_private_key: str
    # Key id, also referred as "kid". | MaxLen: 127
    gck_keyid: str
    # Lifetime of automatically generated access tokens in minutes | Default: 60 | Min: 1 | Max: 3600
    gck_access_token_lifetime: int
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> CloudServicePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class CloudService:
    """
    Configure system cloud service.
    
    Path: system/cloud_service
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
    ) -> CloudServiceResponse: ...
    
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
    ) -> CloudServiceResponse: ...
    
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
    ) -> list[CloudServiceResponse]: ...
    
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
    ) -> CloudServiceObject: ...
    
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
    ) -> CloudServiceObject: ...
    
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
    ) -> list[CloudServiceObject]: ...
    
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
    ) -> CloudServiceResponse: ...
    
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
    ) -> CloudServiceResponse: ...
    
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
    ) -> list[CloudServiceResponse]: ...
    
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
    ) -> CloudServiceObject | list[CloudServiceObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CloudServiceObject: ...
    
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CloudServiceObject: ...
    
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
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
    ) -> CloudServiceObject: ...
    
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
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
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

class CloudServiceDictMode:
    """CloudService endpoint for dict response mode (default for this client).
    
    By default returns CloudServiceResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return CloudServiceObject.
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
    ) -> CloudServiceObject: ...
    
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
    ) -> list[CloudServiceObject]: ...
    
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
    ) -> CloudServiceResponse: ...
    
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
    ) -> list[CloudServiceResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CloudServiceObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CloudServiceObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
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
    ) -> CloudServiceObject: ...
    
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
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
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


class CloudServiceObjectMode:
    """CloudService endpoint for object response mode (default for this client).
    
    By default returns CloudServiceObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return CloudServiceResponse (TypedDict).
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
    ) -> CloudServiceResponse: ...
    
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
    ) -> list[CloudServiceResponse]: ...
    
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
    ) -> CloudServiceObject: ...
    
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
    ) -> list[CloudServiceObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CloudServiceObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> CloudServiceObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> CloudServiceObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> CloudServiceObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
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
    ) -> CloudServiceObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> CloudServiceObject: ...
    
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
        payload_dict: CloudServicePayload | None = ...,
        name: str | None = ...,
        vendor: Literal["unknown", "google-cloud-kms"] | None = ...,
        traffic_vdom: str | None = ...,
        gck_service_account: str | None = ...,
        gck_private_key: str | None = ...,
        gck_keyid: str | None = ...,
        gck_access_token_lifetime: int | None = ...,
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
    "CloudService",
    "CloudServiceDictMode",
    "CloudServiceObjectMode",
    "CloudServicePayload",
    "CloudServiceObject",
]