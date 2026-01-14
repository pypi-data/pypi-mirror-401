from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class HsmLocalPayload(TypedDict, total=False):
    """
    Type hints for certificate/hsm_local payload fields.
    
    Local certificates whose keys are stored on HSM.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.cloud-service.CloudServiceEndpoint` (via: gch-cloud-service-name)

    **Usage:**
        payload: HsmLocalPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Name. | MaxLen: 35
    comments: str  # Comment. | MaxLen: 511
    vendor: Literal["unknown", "gch"]  # HSM vendor. | Default: unknown
    api_version: Literal["unknown", "gch-default"]  # API version for communicating with HSM. | Default: unknown
    certificate: str  # PEM format certificate.
    range: Literal["global", "vdom"]  # Either a global or VDOM IP address range for the c | Default: global
    source: Literal["factory", "user", "bundle"]  # Certificate source type. | Default: user
    gch_url: str  # Google Cloud HSM key URL | MaxLen: 1024
    gch_project: str  # Google Cloud HSM project ID. | MaxLen: 31
    gch_location: str  # Google Cloud HSM location. | MaxLen: 63
    gch_keyring: str  # Google Cloud HSM keyring. | MaxLen: 63
    gch_cryptokey: str  # Google Cloud HSM cryptokey. | MaxLen: 63
    gch_cryptokey_version: str  # Google Cloud HSM cryptokey version. | MaxLen: 31
    gch_cloud_service_name: str  # Cloud service config name to generate access token | MaxLen: 35
    gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"]  # Google Cloud HSM cryptokey algorithm. | Default: rsa-sign-pkcs1-2048-sha256
    details: str  # Print hsm-local certificate detailed information.

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class HsmLocalResponse(TypedDict):
    """
    Type hints for certificate/hsm_local API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Name. | MaxLen: 35
    comments: str  # Comment. | MaxLen: 511
    vendor: Literal["unknown", "gch"]  # HSM vendor. | Default: unknown
    api_version: Literal["unknown", "gch-default"]  # API version for communicating with HSM. | Default: unknown
    certificate: str  # PEM format certificate.
    range: Literal["global", "vdom"]  # Either a global or VDOM IP address range for the c | Default: global
    source: Literal["factory", "user", "bundle"]  # Certificate source type. | Default: user
    gch_url: str  # Google Cloud HSM key URL | MaxLen: 1024
    gch_project: str  # Google Cloud HSM project ID. | MaxLen: 31
    gch_location: str  # Google Cloud HSM location. | MaxLen: 63
    gch_keyring: str  # Google Cloud HSM keyring. | MaxLen: 63
    gch_cryptokey: str  # Google Cloud HSM cryptokey. | MaxLen: 63
    gch_cryptokey_version: str  # Google Cloud HSM cryptokey version. | MaxLen: 31
    gch_cloud_service_name: str  # Cloud service config name to generate access token | MaxLen: 35
    gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"]  # Google Cloud HSM cryptokey algorithm. | Default: rsa-sign-pkcs1-2048-sha256
    details: str  # Print hsm-local certificate detailed information.


@final
class HsmLocalObject:
    """Typed FortiObject for certificate/hsm_local with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Name. | MaxLen: 35
    name: str
    # Comment. | MaxLen: 511
    comments: str
    # HSM vendor. | Default: unknown
    vendor: Literal["unknown", "gch"]
    # API version for communicating with HSM. | Default: unknown
    api_version: Literal["unknown", "gch-default"]
    # PEM format certificate.
    certificate: str
    # Either a global or VDOM IP address range for the certificate | Default: global
    range: Literal["global", "vdom"]
    # Certificate source type. | Default: user
    source: Literal["factory", "user", "bundle"]
    # Google Cloud HSM key URL | MaxLen: 1024
    gch_url: str
    # Google Cloud HSM project ID. | MaxLen: 31
    gch_project: str
    # Google Cloud HSM location. | MaxLen: 63
    gch_location: str
    # Google Cloud HSM keyring. | MaxLen: 63
    gch_keyring: str
    # Google Cloud HSM cryptokey. | MaxLen: 63
    gch_cryptokey: str
    # Google Cloud HSM cryptokey version. | MaxLen: 31
    gch_cryptokey_version: str
    # Cloud service config name to generate access token. | MaxLen: 35
    gch_cloud_service_name: str
    # Google Cloud HSM cryptokey algorithm. | Default: rsa-sign-pkcs1-2048-sha256
    gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"]
    # Print hsm-local certificate detailed information.
    details: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> HsmLocalPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class HsmLocal:
    """
    Local certificates whose keys are stored on HSM.
    
    Path: certificate/hsm_local
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
    ) -> HsmLocalResponse: ...
    
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
    ) -> HsmLocalResponse: ...
    
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
    ) -> list[HsmLocalResponse]: ...
    
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
    ) -> HsmLocalObject: ...
    
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
    ) -> HsmLocalObject: ...
    
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
    ) -> list[HsmLocalObject]: ...
    
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
    ) -> HsmLocalResponse: ...
    
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
    ) -> HsmLocalResponse: ...
    
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
    ) -> list[HsmLocalResponse]: ...
    
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
    ) -> HsmLocalObject | list[HsmLocalObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HsmLocalObject: ...
    
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HsmLocalObject: ...
    
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
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
    ) -> HsmLocalObject: ...
    
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
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
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

class HsmLocalDictMode:
    """HsmLocal endpoint for dict response mode (default for this client).
    
    By default returns HsmLocalResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return HsmLocalObject.
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
    ) -> HsmLocalObject: ...
    
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
    ) -> list[HsmLocalObject]: ...
    
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
    ) -> HsmLocalResponse: ...
    
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
    ) -> list[HsmLocalResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HsmLocalObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HsmLocalObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
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
    ) -> HsmLocalObject: ...
    
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
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
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


class HsmLocalObjectMode:
    """HsmLocal endpoint for object response mode (default for this client).
    
    By default returns HsmLocalObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return HsmLocalResponse (TypedDict).
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
    ) -> HsmLocalResponse: ...
    
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
    ) -> list[HsmLocalResponse]: ...
    
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
    ) -> HsmLocalObject: ...
    
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
    ) -> list[HsmLocalObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HsmLocalObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> HsmLocalObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> HsmLocalObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> HsmLocalObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
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
    ) -> HsmLocalObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> HsmLocalObject: ...
    
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
        payload_dict: HsmLocalPayload | None = ...,
        name: str | None = ...,
        comments: str | None = ...,
        vendor: Literal["unknown", "gch"] | None = ...,
        api_version: Literal["unknown", "gch-default"] | None = ...,
        certificate: str | None = ...,
        range: Literal["global", "vdom"] | None = ...,
        source: Literal["factory", "user", "bundle"] | None = ...,
        gch_url: str | None = ...,
        gch_project: str | None = ...,
        gch_location: str | None = ...,
        gch_keyring: str | None = ...,
        gch_cryptokey: str | None = ...,
        gch_cryptokey_version: str | None = ...,
        gch_cloud_service_name: str | None = ...,
        gch_cryptokey_algorithm: Literal["rsa-sign-pkcs1-2048-sha256", "rsa-sign-pkcs1-3072-sha256", "rsa-sign-pkcs1-4096-sha256", "rsa-sign-pkcs1-4096-sha512", "rsa-sign-pss-2048-sha256", "rsa-sign-pss-3072-sha256", "rsa-sign-pss-4096-sha256", "rsa-sign-pss-4096-sha512", "ec-sign-p256-sha256", "ec-sign-p384-sha384", "ec-sign-secp256k1-sha256"] | None = ...,
        details: str | None = ...,
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
    "HsmLocal",
    "HsmLocalDictMode",
    "HsmLocalObjectMode",
    "HsmLocalPayload",
    "HsmLocalObject",
]