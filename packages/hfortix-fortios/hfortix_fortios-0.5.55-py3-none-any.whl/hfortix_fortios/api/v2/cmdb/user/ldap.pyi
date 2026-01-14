from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class LdapPayload(TypedDict, total=False):
    """
    Type hints for user/ldap payload fields.
    
    Configure LDAP server entries.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.system.interface.InterfaceEndpoint` (via: interface, source-ip-interface)
        - :class:`~.user.exchange.ExchangeEndpoint` (via: user-info-exchange-server)
        - :class:`~.vpn.certificate.ca.CaEndpoint` (via: ca-cert)
        - :class:`~.vpn.certificate.local.LocalEndpoint` (via: client-cert)

    **Usage:**
        payload: LdapPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # LDAP server entry name. | MaxLen: 35
    server: str  # LDAP server CN domain name or IP. | MaxLen: 63
    secondary_server: str  # Secondary LDAP server CN domain name or IP. | MaxLen: 63
    tertiary_server: str  # Tertiary LDAP server CN domain name or IP. | MaxLen: 63
    status_ttl: int  # Time for which server reachability is cached so th | Default: 300 | Min: 0 | Max: 600
    server_identity_check: Literal["enable", "disable"]  # Enable/disable LDAP server identity check | Default: enable
    source_ip: str  # FortiGate IP address to be used for communication | MaxLen: 63
    source_ip_interface: str  # Source interface for communication with the LDAP s | MaxLen: 15
    source_port: int  # Source port to be used for communication with the | Default: 0 | Min: 0 | Max: 65535
    cnid: str  # Common name identifier for the LDAP server. The co | Default: cn | MaxLen: 20
    dn: str  # Distinguished name used to look up entries on the | MaxLen: 511
    type: Literal["simple", "anonymous", "regular"]  # Authentication type for LDAP searches. | Default: simple
    two_factor: Literal["disable", "fortitoken-cloud"]  # Enable/disable two-factor authentication. | Default: disable
    two_factor_authentication: Literal["fortitoken", "email", "sms"]  # Authentication method by FortiToken Cloud.
    two_factor_notification: Literal["email", "sms"]  # Notification method for user activation by FortiTo
    two_factor_filter: str  # Filter used to synchronize users to FortiToken Clo | MaxLen: 2047
    username: str  # Username (full DN) for initial binding. | MaxLen: 511
    password: str  # Password for initial binding. | MaxLen: 128
    group_member_check: Literal["user-attr", "group-object", "posix-group-object"]  # Group member checking methods. | Default: user-attr
    group_search_base: str  # Search base used for group searching. | MaxLen: 511
    group_object_filter: str  # Filter used for group searching. | Default: (&(objectcategory=group)(member=*)) | MaxLen: 2047
    group_filter: str  # Filter used for group matching. | MaxLen: 2047
    secure: Literal["disable", "starttls", "ldaps"]  # Port to be used for authentication. | Default: disable
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]  # Minimum supported protocol version for SSL/TLS con | Default: default
    ca_cert: str  # CA certificate name. | MaxLen: 79
    port: int  # Port to be used for communication with the LDAP se | Default: 389 | Min: 1 | Max: 65535
    password_expiry_warning: Literal["enable", "disable"]  # Enable/disable password expiry warnings. | Default: disable
    password_renewal: Literal["enable", "disable"]  # Enable/disable online password renewal. | Default: disable
    member_attr: str  # Name of attribute from which to get group membersh | Default: memberOf | MaxLen: 63
    account_key_processing: Literal["same", "strip"]  # Account key processing operation. The FortiGate wi | Default: same
    account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"]  # Define subject identity field in certificate for u | Default: othername
    account_key_filter: str  # Account key filter, using the UPN as the search fi | Default: (&(userPrincipalName=%s)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))) | MaxLen: 2047
    search_type: Literal["recursive"]  # Search type.
    client_cert_auth: Literal["enable", "disable"]  # Enable/disable using client certificate for TLS au | Default: disable
    client_cert: str  # Client certificate name. | MaxLen: 79
    obtain_user_info: Literal["enable", "disable"]  # Enable/disable obtaining of user information. | Default: enable
    user_info_exchange_server: str  # MS Exchange server from which to fetch user inform | MaxLen: 35
    interface_select_method: Literal["auto", "sdwan", "specify"]  # Specify how to select outgoing interface to reach | Default: auto
    interface: str  # Specify outgoing interface to reach server. | MaxLen: 15
    vrf_select: int  # VRF ID used for connection to server. | Default: 0 | Min: 0 | Max: 511
    antiphish: Literal["enable", "disable"]  # Enable/disable AntiPhishing credential backend. | Default: disable
    password_attr: str  # Name of attribute to get password hash. | Default: userPassword | MaxLen: 35

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class LdapResponse(TypedDict):
    """
    Type hints for user/ldap API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # LDAP server entry name. | MaxLen: 35
    server: str  # LDAP server CN domain name or IP. | MaxLen: 63
    secondary_server: str  # Secondary LDAP server CN domain name or IP. | MaxLen: 63
    tertiary_server: str  # Tertiary LDAP server CN domain name or IP. | MaxLen: 63
    status_ttl: int  # Time for which server reachability is cached so th | Default: 300 | Min: 0 | Max: 600
    server_identity_check: Literal["enable", "disable"]  # Enable/disable LDAP server identity check | Default: enable
    source_ip: str  # FortiGate IP address to be used for communication | MaxLen: 63
    source_ip_interface: str  # Source interface for communication with the LDAP s | MaxLen: 15
    source_port: int  # Source port to be used for communication with the | Default: 0 | Min: 0 | Max: 65535
    cnid: str  # Common name identifier for the LDAP server. The co | Default: cn | MaxLen: 20
    dn: str  # Distinguished name used to look up entries on the | MaxLen: 511
    type: Literal["simple", "anonymous", "regular"]  # Authentication type for LDAP searches. | Default: simple
    two_factor: Literal["disable", "fortitoken-cloud"]  # Enable/disable two-factor authentication. | Default: disable
    two_factor_authentication: Literal["fortitoken", "email", "sms"]  # Authentication method by FortiToken Cloud.
    two_factor_notification: Literal["email", "sms"]  # Notification method for user activation by FortiTo
    two_factor_filter: str  # Filter used to synchronize users to FortiToken Clo | MaxLen: 2047
    username: str  # Username (full DN) for initial binding. | MaxLen: 511
    password: str  # Password for initial binding. | MaxLen: 128
    group_member_check: Literal["user-attr", "group-object", "posix-group-object"]  # Group member checking methods. | Default: user-attr
    group_search_base: str  # Search base used for group searching. | MaxLen: 511
    group_object_filter: str  # Filter used for group searching. | Default: (&(objectcategory=group)(member=*)) | MaxLen: 2047
    group_filter: str  # Filter used for group matching. | MaxLen: 2047
    secure: Literal["disable", "starttls", "ldaps"]  # Port to be used for authentication. | Default: disable
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]  # Minimum supported protocol version for SSL/TLS con | Default: default
    ca_cert: str  # CA certificate name. | MaxLen: 79
    port: int  # Port to be used for communication with the LDAP se | Default: 389 | Min: 1 | Max: 65535
    password_expiry_warning: Literal["enable", "disable"]  # Enable/disable password expiry warnings. | Default: disable
    password_renewal: Literal["enable", "disable"]  # Enable/disable online password renewal. | Default: disable
    member_attr: str  # Name of attribute from which to get group membersh | Default: memberOf | MaxLen: 63
    account_key_processing: Literal["same", "strip"]  # Account key processing operation. The FortiGate wi | Default: same
    account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"]  # Define subject identity field in certificate for u | Default: othername
    account_key_filter: str  # Account key filter, using the UPN as the search fi | Default: (&(userPrincipalName=%s)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))) | MaxLen: 2047
    search_type: Literal["recursive"]  # Search type.
    client_cert_auth: Literal["enable", "disable"]  # Enable/disable using client certificate for TLS au | Default: disable
    client_cert: str  # Client certificate name. | MaxLen: 79
    obtain_user_info: Literal["enable", "disable"]  # Enable/disable obtaining of user information. | Default: enable
    user_info_exchange_server: str  # MS Exchange server from which to fetch user inform | MaxLen: 35
    interface_select_method: Literal["auto", "sdwan", "specify"]  # Specify how to select outgoing interface to reach | Default: auto
    interface: str  # Specify outgoing interface to reach server. | MaxLen: 15
    vrf_select: int  # VRF ID used for connection to server. | Default: 0 | Min: 0 | Max: 511
    antiphish: Literal["enable", "disable"]  # Enable/disable AntiPhishing credential backend. | Default: disable
    password_attr: str  # Name of attribute to get password hash. | Default: userPassword | MaxLen: 35


@final
class LdapObject:
    """Typed FortiObject for user/ldap with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # LDAP server entry name. | MaxLen: 35
    name: str
    # LDAP server CN domain name or IP. | MaxLen: 63
    server: str
    # Secondary LDAP server CN domain name or IP. | MaxLen: 63
    secondary_server: str
    # Tertiary LDAP server CN domain name or IP. | MaxLen: 63
    tertiary_server: str
    # Time for which server reachability is cached so that when a | Default: 300 | Min: 0 | Max: 600
    status_ttl: int
    # Enable/disable LDAP server identity check | Default: enable
    server_identity_check: Literal["enable", "disable"]
    # FortiGate IP address to be used for communication with the L | MaxLen: 63
    source_ip: str
    # Source interface for communication with the LDAP server. | MaxLen: 15
    source_ip_interface: str
    # Source port to be used for communication with the LDAP serve | Default: 0 | Min: 0 | Max: 65535
    source_port: int
    # Common name identifier for the LDAP server. The common name | Default: cn | MaxLen: 20
    cnid: str
    # Distinguished name used to look up entries on the LDAP serve | MaxLen: 511
    dn: str
    # Authentication type for LDAP searches. | Default: simple
    type: Literal["simple", "anonymous", "regular"]
    # Enable/disable two-factor authentication. | Default: disable
    two_factor: Literal["disable", "fortitoken-cloud"]
    # Authentication method by FortiToken Cloud.
    two_factor_authentication: Literal["fortitoken", "email", "sms"]
    # Notification method for user activation by FortiToken Cloud.
    two_factor_notification: Literal["email", "sms"]
    # Filter used to synchronize users to FortiToken Cloud. | MaxLen: 2047
    two_factor_filter: str
    # Username (full DN) for initial binding. | MaxLen: 511
    username: str
    # Password for initial binding. | MaxLen: 128
    password: str
    # Group member checking methods. | Default: user-attr
    group_member_check: Literal["user-attr", "group-object", "posix-group-object"]
    # Search base used for group searching. | MaxLen: 511
    group_search_base: str
    # Filter used for group searching. | Default: (&(objectcategory=group)(member=*)) | MaxLen: 2047
    group_object_filter: str
    # Filter used for group matching. | MaxLen: 2047
    group_filter: str
    # Port to be used for authentication. | Default: disable
    secure: Literal["disable", "starttls", "ldaps"]
    # Minimum supported protocol version for SSL/TLS connections | Default: default
    ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"]
    # CA certificate name. | MaxLen: 79
    ca_cert: str
    # Port to be used for communication with the LDAP server | Default: 389 | Min: 1 | Max: 65535
    port: int
    # Enable/disable password expiry warnings. | Default: disable
    password_expiry_warning: Literal["enable", "disable"]
    # Enable/disable online password renewal. | Default: disable
    password_renewal: Literal["enable", "disable"]
    # Name of attribute from which to get group membership. | Default: memberOf | MaxLen: 63
    member_attr: str
    # Account key processing operation. The FortiGate will keep ei | Default: same
    account_key_processing: Literal["same", "strip"]
    # Define subject identity field in certificate for user access | Default: othername
    account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"]
    # Account key filter, using the UPN as the search filter. | Default: (&(userPrincipalName=%s)(!(UserAccountControl:1.2.840.113556.1.4.803:=2))) | MaxLen: 2047
    account_key_filter: str
    # Search type.
    search_type: Literal["recursive"]
    # Enable/disable using client certificate for TLS authenticati | Default: disable
    client_cert_auth: Literal["enable", "disable"]
    # Client certificate name. | MaxLen: 79
    client_cert: str
    # Enable/disable obtaining of user information. | Default: enable
    obtain_user_info: Literal["enable", "disable"]
    # MS Exchange server from which to fetch user information. | MaxLen: 35
    user_info_exchange_server: str
    # Specify how to select outgoing interface to reach server. | Default: auto
    interface_select_method: Literal["auto", "sdwan", "specify"]
    # Specify outgoing interface to reach server. | MaxLen: 15
    interface: str
    # VRF ID used for connection to server. | Default: 0 | Min: 0 | Max: 511
    vrf_select: int
    # Enable/disable AntiPhishing credential backend. | Default: disable
    antiphish: Literal["enable", "disable"]
    # Name of attribute to get password hash. | Default: userPassword | MaxLen: 35
    password_attr: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> LdapPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Ldap:
    """
    Configure LDAP server entries.
    
    Path: user/ldap
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
    ) -> LdapResponse: ...
    
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
    ) -> LdapResponse: ...
    
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
    ) -> list[LdapResponse]: ...
    
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
    ) -> LdapObject: ...
    
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
    ) -> LdapObject: ...
    
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
    ) -> list[LdapObject]: ...
    
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
    ) -> LdapResponse: ...
    
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
    ) -> LdapResponse: ...
    
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
    ) -> list[LdapResponse]: ...
    
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
    ) -> LdapObject | list[LdapObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LdapObject: ...
    
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LdapObject: ...
    
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
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
    ) -> LdapObject: ...
    
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
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
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

class LdapDictMode:
    """Ldap endpoint for dict response mode (default for this client).
    
    By default returns LdapResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return LdapObject.
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
    ) -> LdapObject: ...
    
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
    ) -> list[LdapObject]: ...
    
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
    ) -> LdapResponse: ...
    
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
    ) -> list[LdapResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LdapObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LdapObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
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
    ) -> LdapObject: ...
    
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
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
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


class LdapObjectMode:
    """Ldap endpoint for object response mode (default for this client).
    
    By default returns LdapObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return LdapResponse (TypedDict).
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
    ) -> LdapResponse: ...
    
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
    ) -> list[LdapResponse]: ...
    
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
    ) -> LdapObject: ...
    
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
    ) -> list[LdapObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LdapObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LdapObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> LdapObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LdapObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
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
    ) -> LdapObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> LdapObject: ...
    
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
        payload_dict: LdapPayload | None = ...,
        name: str | None = ...,
        server: str | None = ...,
        secondary_server: str | None = ...,
        tertiary_server: str | None = ...,
        status_ttl: int | None = ...,
        server_identity_check: Literal["enable", "disable"] | None = ...,
        source_ip: str | None = ...,
        source_ip_interface: str | None = ...,
        source_port: int | None = ...,
        cnid: str | None = ...,
        dn: str | None = ...,
        type: Literal["simple", "anonymous", "regular"] | None = ...,
        two_factor: Literal["disable", "fortitoken-cloud"] | None = ...,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = ...,
        two_factor_notification: Literal["email", "sms"] | None = ...,
        two_factor_filter: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        group_member_check: Literal["user-attr", "group-object", "posix-group-object"] | None = ...,
        group_search_base: str | None = ...,
        group_object_filter: str | None = ...,
        group_filter: str | None = ...,
        secure: Literal["disable", "starttls", "ldaps"] | None = ...,
        ssl_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = ...,
        ca_cert: str | None = ...,
        port: int | None = ...,
        password_expiry_warning: Literal["enable", "disable"] | None = ...,
        password_renewal: Literal["enable", "disable"] | None = ...,
        member_attr: str | None = ...,
        account_key_processing: Literal["same", "strip"] | None = ...,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = ...,
        account_key_filter: str | None = ...,
        search_type: Literal["recursive"] | list[str] | None = ...,
        client_cert_auth: Literal["enable", "disable"] | None = ...,
        client_cert: str | None = ...,
        obtain_user_info: Literal["enable", "disable"] | None = ...,
        user_info_exchange_server: str | None = ...,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = ...,
        interface: str | None = ...,
        vrf_select: int | None = ...,
        antiphish: Literal["enable", "disable"] | None = ...,
        password_attr: str | None = ...,
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
    "Ldap",
    "LdapDictMode",
    "LdapObjectMode",
    "LdapPayload",
    "LdapObject",
]