from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class AcmePayload(TypedDict, total=False):
    """
    Type hints for system/acme payload fields.
    
    Configure ACME client.
    
    **Usage:**
        payload: AcmePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    interface: list[dict[str, Any]]  # Interface(s) on which the ACME client will listen
    use_ha_direct: Literal["enable", "disable"]  # Enable the use of 'ha-mgmt' interface to connect t | Default: disable
    source_ip: str  # Source IPv4 address used to connect to the ACME se | Default: 0.0.0.0
    source_ip6: str  # Source IPv6 address used to connect to the ACME se | Default: ::
    accounts: list[dict[str, Any]]  # ACME accounts list.
    acc_details: str  # Print Account information and decrypted key.
    status: str  # Print information about the current status of the

# Nested TypedDicts for table field children (dict mode)

class AcmeInterfaceItem(TypedDict):
    """Type hints for interface table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    interface_name: str  # Interface name. | MaxLen: 79


class AcmeAccountsItem(TypedDict):
    """Type hints for accounts table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    id: str  # Account id. | MaxLen: 255
    status: str  # Account status. | MaxLen: 127
    url: str  # Account url. | MaxLen: 511
    ca_url: str  # Account ca_url. | MaxLen: 255
    email: str  # Account email. | MaxLen: 255
    eab_key_id: str  # External Acccount Binding Key ID. | MaxLen: 255
    eab_key_hmac: str  # External Acccount Binding Key HMAC. | MaxLen: 128
    privatekey: str  # Account Private Key. | MaxLen: 8191


# Nested classes for table field children (object mode)

@final
class AcmeInterfaceObject:
    """Typed object for interface table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Interface name. | MaxLen: 79
    interface_name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class AcmeAccountsObject:
    """Typed object for accounts table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Account id. | MaxLen: 255
    id: str
    # Account status. | MaxLen: 127
    status: str
    # Account url. | MaxLen: 511
    url: str
    # Account ca_url. | MaxLen: 255
    ca_url: str
    # Account email. | MaxLen: 255
    email: str
    # External Acccount Binding Key ID. | MaxLen: 255
    eab_key_id: str
    # External Acccount Binding Key HMAC. | MaxLen: 128
    eab_key_hmac: str
    # Account Private Key. | MaxLen: 8191
    privatekey: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class AcmeResponse(TypedDict):
    """
    Type hints for system/acme API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    interface: list[AcmeInterfaceItem]  # Interface(s) on which the ACME client will listen
    use_ha_direct: Literal["enable", "disable"]  # Enable the use of 'ha-mgmt' interface to connect t | Default: disable
    source_ip: str  # Source IPv4 address used to connect to the ACME se | Default: 0.0.0.0
    source_ip6: str  # Source IPv6 address used to connect to the ACME se | Default: ::
    accounts: list[AcmeAccountsItem]  # ACME accounts list.
    acc_details: str  # Print Account information and decrypted key.
    status: str  # Print information about the current status of the


@final
class AcmeObject:
    """Typed FortiObject for system/acme with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Interface(s) on which the ACME client will listen for challe
    interface: list[AcmeInterfaceObject]
    # Enable the use of 'ha-mgmt' interface to connect to the ACME | Default: disable
    use_ha_direct: Literal["enable", "disable"]
    # Source IPv4 address used to connect to the ACME server. | Default: 0.0.0.0
    source_ip: str
    # Source IPv6 address used to connect to the ACME server. | Default: ::
    source_ip6: str
    # ACME accounts list.
    accounts: list[AcmeAccountsObject]
    # Print Account information and decrypted key.
    acc_details: str
    # Print information about the current status of the acme clien
    status: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> AcmePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Acme:
    """
    Configure ACME client.
    
    Path: system/acme
    Category: cmdb
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
    ) -> AcmeResponse: ...
    
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
    ) -> AcmeResponse: ...
    
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
    ) -> AcmeResponse: ...
    
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
    ) -> AcmeObject: ...
    
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
    ) -> AcmeObject: ...
    
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
    ) -> AcmeObject: ...
    
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
    ) -> AcmeResponse: ...
    
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
    ) -> AcmeResponse: ...
    
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
    ) -> AcmeResponse: ...
    
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
    ) -> dict[str, Any] | FortiObject: ...
    
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
    ) -> AcmeObject | dict[str, Any]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AcmeObject: ...
    
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
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

class AcmeDictMode:
    """Acme endpoint for dict response mode (default for this client).
    
    By default returns AcmeResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return AcmeObject.
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
    ) -> AcmeObject: ...
    
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
    ) -> AcmeObject: ...
    
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
    ) -> AcmeResponse: ...
    
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
    ) -> AcmeResponse: ...


    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AcmeObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
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
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
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


class AcmeObjectMode:
    """Acme endpoint for object response mode (default for this client).
    
    By default returns AcmeObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return AcmeResponse (TypedDict).
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
    ) -> AcmeResponse: ...
    
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
    ) -> AcmeResponse: ...
    
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
    ) -> AcmeObject: ...
    
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
    ) -> AcmeObject: ...


    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> AcmeObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> AcmeObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
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
        payload_dict: AcmePayload | None = ...,
        interface: str | list[str] | list[dict[str, Any]] | None = ...,
        use_ha_direct: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip6: str | None = ...,
        accounts: str | list[str] | list[dict[str, Any]] | None = ...,
        acc_details: str | None = ...,
        status: str | None = ...,
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
    "Acme",
    "AcmeDictMode",
    "AcmeObjectMode",
    "AcmePayload",
    "AcmeObject",
]