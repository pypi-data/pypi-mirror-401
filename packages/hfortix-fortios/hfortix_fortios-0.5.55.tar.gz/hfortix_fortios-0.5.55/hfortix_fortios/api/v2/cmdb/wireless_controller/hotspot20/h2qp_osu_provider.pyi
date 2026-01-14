from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class H2qpOsuProviderPayload(TypedDict, total=False):
    """
    Type hints for wireless_controller/hotspot20/h2qp_osu_provider payload fields.
    
    Configure online sign up (OSU) provider list.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.wireless-controller.hotspot20.icon.IconEndpoint` (via: icon)

    **Usage:**
        payload: H2qpOsuProviderPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # OSU provider ID. | MaxLen: 35
    friendly_name: list[dict[str, Any]]  # OSU provider friendly name.
    server_uri: str  # Server URI. | MaxLen: 255
    osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"]  # OSU method list.
    osu_nai: str  # OSU NAI. | MaxLen: 255
    service_description: list[dict[str, Any]]  # OSU service name.
    icon: str  # OSU provider icon. | MaxLen: 35

# Nested TypedDicts for table field children (dict mode)

class H2qpOsuProviderFriendlynameItem(TypedDict):
    """Type hints for friendly-name table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    index: int  # OSU provider friendly name index. | Default: 0 | Min: 1 | Max: 10
    lang: str  # Language code. | Default: eng | MaxLen: 3
    friendly_name: str  # OSU provider friendly name. | MaxLen: 252


class H2qpOsuProviderServicedescriptionItem(TypedDict):
    """Type hints for service-description table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    service_id: int  # OSU service ID. | Default: 0 | Min: 0 | Max: 4294967295
    lang: str  # Language code. | Default: eng | MaxLen: 3
    service_description: str  # Service description. | MaxLen: 252


# Nested classes for table field children (object mode)

@final
class H2qpOsuProviderFriendlynameObject:
    """Typed object for friendly-name table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # OSU provider friendly name index. | Default: 0 | Min: 1 | Max: 10
    index: int
    # Language code. | Default: eng | MaxLen: 3
    lang: str
    # OSU provider friendly name. | MaxLen: 252
    friendly_name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class H2qpOsuProviderServicedescriptionObject:
    """Typed object for service-description table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # OSU service ID. | Default: 0 | Min: 0 | Max: 4294967295
    service_id: int
    # Language code. | Default: eng | MaxLen: 3
    lang: str
    # Service description. | MaxLen: 252
    service_description: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class H2qpOsuProviderResponse(TypedDict):
    """
    Type hints for wireless_controller/hotspot20/h2qp_osu_provider API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # OSU provider ID. | MaxLen: 35
    friendly_name: list[H2qpOsuProviderFriendlynameItem]  # OSU provider friendly name.
    server_uri: str  # Server URI. | MaxLen: 255
    osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"]  # OSU method list.
    osu_nai: str  # OSU NAI. | MaxLen: 255
    service_description: list[H2qpOsuProviderServicedescriptionItem]  # OSU service name.
    icon: str  # OSU provider icon. | MaxLen: 35


@final
class H2qpOsuProviderObject:
    """Typed FortiObject for wireless_controller/hotspot20/h2qp_osu_provider with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # OSU provider ID. | MaxLen: 35
    name: str
    # OSU provider friendly name.
    friendly_name: list[H2qpOsuProviderFriendlynameObject]
    # Server URI. | MaxLen: 255
    server_uri: str
    # OSU method list.
    osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"]
    # OSU NAI. | MaxLen: 255
    osu_nai: str
    # OSU service name.
    service_description: list[H2qpOsuProviderServicedescriptionObject]
    # OSU provider icon. | MaxLen: 35
    icon: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> H2qpOsuProviderPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class H2qpOsuProvider:
    """
    Configure online sign up (OSU) provider list.
    
    Path: wireless_controller/hotspot20/h2qp_osu_provider
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
    ) -> H2qpOsuProviderResponse: ...
    
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
    ) -> H2qpOsuProviderResponse: ...
    
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
    ) -> list[H2qpOsuProviderResponse]: ...
    
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
    ) -> H2qpOsuProviderObject: ...
    
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
    ) -> H2qpOsuProviderObject: ...
    
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
    ) -> list[H2qpOsuProviderObject]: ...
    
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
    ) -> H2qpOsuProviderResponse: ...
    
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
    ) -> H2qpOsuProviderResponse: ...
    
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
    ) -> list[H2qpOsuProviderResponse]: ...
    
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
    ) -> H2qpOsuProviderObject | list[H2qpOsuProviderObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpOsuProviderObject: ...
    
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpOsuProviderObject: ...
    
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
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
    ) -> H2qpOsuProviderObject: ...
    
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
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
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

class H2qpOsuProviderDictMode:
    """H2qpOsuProvider endpoint for dict response mode (default for this client).
    
    By default returns H2qpOsuProviderResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return H2qpOsuProviderObject.
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
    ) -> H2qpOsuProviderObject: ...
    
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
    ) -> list[H2qpOsuProviderObject]: ...
    
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
    ) -> H2qpOsuProviderResponse: ...
    
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
    ) -> list[H2qpOsuProviderResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpOsuProviderObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpOsuProviderObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
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
    ) -> H2qpOsuProviderObject: ...
    
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
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
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


class H2qpOsuProviderObjectMode:
    """H2qpOsuProvider endpoint for object response mode (default for this client).
    
    By default returns H2qpOsuProviderObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return H2qpOsuProviderResponse (TypedDict).
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
    ) -> H2qpOsuProviderResponse: ...
    
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
    ) -> list[H2qpOsuProviderResponse]: ...
    
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
    ) -> H2qpOsuProviderObject: ...
    
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
    ) -> list[H2qpOsuProviderObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpOsuProviderObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> H2qpOsuProviderObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> H2qpOsuProviderObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> H2qpOsuProviderObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
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
    ) -> H2qpOsuProviderObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> H2qpOsuProviderObject: ...
    
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
        payload_dict: H2qpOsuProviderPayload | None = ...,
        name: str | None = ...,
        friendly_name: str | list[str] | list[dict[str, Any]] | None = ...,
        server_uri: str | None = ...,
        osu_method: Literal["oma-dm", "soap-xml-spp", "reserved"] | list[str] | None = ...,
        osu_nai: str | None = ...,
        service_description: str | list[str] | list[dict[str, Any]] | None = ...,
        icon: str | None = ...,
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
    "H2qpOsuProvider",
    "H2qpOsuProviderDictMode",
    "H2qpOsuProviderObjectMode",
    "H2qpOsuProviderPayload",
    "H2qpOsuProviderObject",
]