from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class DdnsPayload(TypedDict, total=False):
    """
    Type hints for system/ddns payload fields.
    
    Configure DDNS.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.certificate.local.LocalEndpoint` (via: ssl-certificate)

    **Usage:**
        payload: DdnsPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    ddnsid: int  # DDNS ID. | Default: 0 | Min: 0 | Max: 4294967295
    ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"]  # Select a DDNS service provider.
    addr_type: Literal["ipv4", "ipv6"]  # Address type of interface address in DDNS update. | Default: ipv4
    server_type: Literal["ipv4", "ipv6"]  # Address type of the DDNS server. | Default: ipv4
    ddns_server_addr: list[dict[str, Any]]  # Generic DDNS server IP/FQDN list.
    ddns_zone: str  # Zone of your domain name (for example, DDNS.com). | MaxLen: 64
    ddns_ttl: int  # Time-to-live for DDNS packets. | Default: 300 | Min: 60 | Max: 86400
    ddns_auth: Literal["disable", "tsig"]  # Enable/disable TSIG authentication for your DDNS s | Default: disable
    ddns_keyname: str  # DDNS update key name. | MaxLen: 64
    ddns_key: str  # DDNS update key (base 64 encoding).
    ddns_domain: str  # Your fully qualified domain name. For example, you | MaxLen: 64
    ddns_username: str  # DDNS user name. | MaxLen: 64
    ddns_sn: str  # DDNS Serial Number. | MaxLen: 64
    ddns_password: str  # DDNS password. | MaxLen: 128
    use_public_ip: Literal["disable", "enable"]  # Enable/disable use of public IP address. | Default: disable
    update_interval: int  # DDNS update interval | Default: 0 | Min: 60 | Max: 2592000
    clear_text: Literal["disable", "enable"]  # Enable/disable use of clear text connections. | Default: disable
    ssl_certificate: str  # Name of local certificate for SSL connections. | Default: Fortinet_Factory | MaxLen: 35
    bound_ip: str  # Bound IP address. | MaxLen: 46
    monitor_interface: list[dict[str, Any]]  # Monitored interface.

# Nested TypedDicts for table field children (dict mode)

class DdnsDdnsserveraddrItem(TypedDict):
    """Type hints for ddns-server-addr table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    addr: str  # IP address or FQDN of the server. | MaxLen: 256


class DdnsMonitorinterfaceItem(TypedDict):
    """Type hints for monitor-interface table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    interface_name: str  # Interface name. | MaxLen: 79


# Nested classes for table field children (object mode)

@final
class DdnsDdnsserveraddrObject:
    """Typed object for ddns-server-addr table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # IP address or FQDN of the server. | MaxLen: 256
    addr: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


@final
class DdnsMonitorinterfaceObject:
    """Typed object for monitor-interface table items.
    
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



# Response TypedDict for GET returns (all fields present in API response)
class DdnsResponse(TypedDict):
    """
    Type hints for system/ddns API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    ddnsid: int  # DDNS ID. | Default: 0 | Min: 0 | Max: 4294967295
    ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"]  # Select a DDNS service provider.
    addr_type: Literal["ipv4", "ipv6"]  # Address type of interface address in DDNS update. | Default: ipv4
    server_type: Literal["ipv4", "ipv6"]  # Address type of the DDNS server. | Default: ipv4
    ddns_server_addr: list[DdnsDdnsserveraddrItem]  # Generic DDNS server IP/FQDN list.
    ddns_zone: str  # Zone of your domain name (for example, DDNS.com). | MaxLen: 64
    ddns_ttl: int  # Time-to-live for DDNS packets. | Default: 300 | Min: 60 | Max: 86400
    ddns_auth: Literal["disable", "tsig"]  # Enable/disable TSIG authentication for your DDNS s | Default: disable
    ddns_keyname: str  # DDNS update key name. | MaxLen: 64
    ddns_key: str  # DDNS update key (base 64 encoding).
    ddns_domain: str  # Your fully qualified domain name. For example, you | MaxLen: 64
    ddns_username: str  # DDNS user name. | MaxLen: 64
    ddns_sn: str  # DDNS Serial Number. | MaxLen: 64
    ddns_password: str  # DDNS password. | MaxLen: 128
    use_public_ip: Literal["disable", "enable"]  # Enable/disable use of public IP address. | Default: disable
    update_interval: int  # DDNS update interval | Default: 0 | Min: 60 | Max: 2592000
    clear_text: Literal["disable", "enable"]  # Enable/disable use of clear text connections. | Default: disable
    ssl_certificate: str  # Name of local certificate for SSL connections. | Default: Fortinet_Factory | MaxLen: 35
    bound_ip: str  # Bound IP address. | MaxLen: 46
    monitor_interface: list[DdnsMonitorinterfaceItem]  # Monitored interface.


@final
class DdnsObject:
    """Typed FortiObject for system/ddns with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # DDNS ID. | Default: 0 | Min: 0 | Max: 4294967295
    ddnsid: int
    # Select a DDNS service provider.
    ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"]
    # Address type of interface address in DDNS update. | Default: ipv4
    addr_type: Literal["ipv4", "ipv6"]
    # Address type of the DDNS server. | Default: ipv4
    server_type: Literal["ipv4", "ipv6"]
    # Generic DDNS server IP/FQDN list.
    ddns_server_addr: list[DdnsDdnsserveraddrObject]
    # Zone of your domain name (for example, DDNS.com). | MaxLen: 64
    ddns_zone: str
    # Time-to-live for DDNS packets. | Default: 300 | Min: 60 | Max: 86400
    ddns_ttl: int
    # Enable/disable TSIG authentication for your DDNS server. | Default: disable
    ddns_auth: Literal["disable", "tsig"]
    # DDNS update key name. | MaxLen: 64
    ddns_keyname: str
    # DDNS update key (base 64 encoding).
    ddns_key: str
    # Your fully qualified domain name. For example, yourname.ddns | MaxLen: 64
    ddns_domain: str
    # DDNS user name. | MaxLen: 64
    ddns_username: str
    # DDNS Serial Number. | MaxLen: 64
    ddns_sn: str
    # DDNS password. | MaxLen: 128
    ddns_password: str
    # Enable/disable use of public IP address. | Default: disable
    use_public_ip: Literal["disable", "enable"]
    # DDNS update interval (60 - 2592000 sec, 0 means default). | Default: 0 | Min: 60 | Max: 2592000
    update_interval: int
    # Enable/disable use of clear text connections. | Default: disable
    clear_text: Literal["disable", "enable"]
    # Name of local certificate for SSL connections. | Default: Fortinet_Factory | MaxLen: 35
    ssl_certificate: str
    # Bound IP address. | MaxLen: 46
    bound_ip: str
    # Monitored interface.
    monitor_interface: list[DdnsMonitorinterfaceObject]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> DdnsPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Ddns:
    """
    Configure DDNS.
    
    Path: system/ddns
    Category: cmdb
    Primary Key: ddnsid
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
        ddnsid: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> DdnsResponse: ...
    
    # Default mode: mkey as keyword arg -> returns typed dict
    @overload
    def get(
        self,
        *,
        ddnsid: int,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> DdnsResponse: ...
    
    # Default mode: no mkey -> returns list of typed dicts
    @overload
    def get(
        self,
        ddnsid: None = None,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[DdnsResponse]: ...
    
    # ================================================================
    # EXPLICIT response_mode="object" OVERLOADS
    # ================================================================
    
    # Object mode: mkey as positional arg -> returns single object
    @overload
    def get(
        self,
        ddnsid: int,
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
    ) -> DdnsObject: ...
    
    # Object mode: mkey as keyword arg -> returns single object
    @overload
    def get(
        self,
        *,
        ddnsid: int,
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
    ) -> DdnsObject: ...
    
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
    ) -> list[DdnsObject]: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def get(
        self,
        ddnsid: int | None = ...,
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
        ddnsid: int,
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
    ) -> DdnsResponse: ...
    
    # Dict mode with mkey provided as keyword arg (single dict)
    @overload
    def get(
        self,
        *,
        ddnsid: int,
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
    ) -> DdnsResponse: ...
    
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
    ) -> list[DdnsResponse]: ...
    
    # Fallback overload for all other cases
    @overload
    def get(
        self,
        ddnsid: int | None = ...,
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
        ddnsid: int | None = ...,
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
    ) -> DdnsObject | list[DdnsObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE overloads
    @overload
    def delete(
        self,
        ddnsid: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    @overload
    def delete(
        self,
        ddnsid: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def delete(
        self,
        ddnsid: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def delete(
        self,
        ddnsid: int | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def delete(
        self,
        ddnsid: int | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def exists(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
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

class DdnsDictMode:
    """Ddns endpoint for dict response mode (default for this client).
    
    By default returns DdnsResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return DdnsObject.
    """
    
    # raw_json=True returns RawAPIResponse regardless of response_mode
    @overload
    def get(
        self,
        ddnsid: int | None = ...,
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
        ddnsid: int,
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
    ) -> DdnsObject: ...
    
    # Object mode override without mkey (list)
    @overload
    def get(
        self,
        ddnsid: None = ...,
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
    ) -> list[DdnsObject]: ...
    
    # Dict mode with mkey (single item) - default
    @overload
    def get(
        self,
        ddnsid: int,
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
    ) -> DdnsResponse: ...
    
    # Dict mode without mkey (list) - default
    @overload
    def get(
        self,
        ddnsid: None = ...,
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
    ) -> list[DdnsResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Object mode override
    @overload
    def delete(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    # DELETE - Default overload (returns MutationResponse)
    @overload
    def delete(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Dict mode (default for DictMode class)
    def delete(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
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


class DdnsObjectMode:
    """Ddns endpoint for object response mode (default for this client).
    
    By default returns DdnsObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return DdnsResponse (TypedDict).
    """
    
    # raw_json=True returns RawAPIResponse for GET
    @overload
    def get(
        self,
        ddnsid: int | None = ...,
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
        ddnsid: int,
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
    ) -> DdnsResponse: ...
    
    # Dict mode override without mkey (list)
    @overload
    def get(
        self,
        ddnsid: None = ...,
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
    ) -> list[DdnsResponse]: ...
    
    # Object mode with mkey (single item) - default
    @overload
    def get(
        self,
        ddnsid: int,
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
    ) -> DdnsObject: ...
    
    # Object mode without mkey (list) - default
    @overload
    def get(
        self,
        ddnsid: None = ...,
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
    ) -> list[DdnsObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for DELETE
    @overload
    def delete(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # DELETE - Dict mode override
    @overload
    def delete(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # DELETE - Object mode override (requires explicit response_mode="object")
    @overload
    def delete(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> DdnsObject: ...
    
    # DELETE - Default for ObjectMode (returns MutationResponse like DictMode)
    def delete(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # Helper methods (inherited from base class)
    def exists(
        self,
        ddnsid: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: DdnsPayload | None = ...,
        ddnsid: int | None = ...,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = ...,
        addr_type: Literal["ipv4", "ipv6"] | None = ...,
        server_type: Literal["ipv4", "ipv6"] | None = ...,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = ...,
        ddns_zone: str | None = ...,
        ddns_ttl: int | None = ...,
        ddns_auth: Literal["disable", "tsig"] | None = ...,
        ddns_keyname: str | None = ...,
        ddns_key: str | None = ...,
        ddns_domain: str | None = ...,
        ddns_username: str | None = ...,
        ddns_sn: str | None = ...,
        ddns_password: str | None = ...,
        use_public_ip: Literal["disable", "enable"] | None = ...,
        update_interval: int | None = ...,
        clear_text: Literal["disable", "enable"] | None = ...,
        ssl_certificate: str | None = ...,
        bound_ip: str | None = ...,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = ...,
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
    "Ddns",
    "DdnsDictMode",
    "DdnsObjectMode",
    "DdnsPayload",
    "DdnsObject",
]