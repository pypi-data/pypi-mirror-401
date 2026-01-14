from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class SchemePayload(TypedDict, total=False):
    """
    Type hints for authentication/scheme payload fields.
    
    Configure Authentication Schemes.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.firewall.ssh.local-ca.LocalCaEndpoint` (via: ssh-ca)
        - :class:`~.user.domain-controller.DomainControllerEndpoint` (via: domain-controller)
        - :class:`~.user.external-identity-provider.ExternalIdentityProviderEndpoint` (via: external-idp)
        - :class:`~.user.fsso.FssoEndpoint` (via: fsso-agent-for-ntlm)
        - :class:`~.user.krb-keytab.KrbKeytabEndpoint` (via: kerberos-keytab)
        - :class:`~.user.saml.SamlEndpoint` (via: saml-server)

    **Usage:**
        payload: SchemePayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # Authentication scheme name. | MaxLen: 35
    method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"]  # Authentication methods (default = basic).
    negotiate_ntlm: Literal["enable", "disable"]  # Enable/disable negotiate authentication for NTLM | Default: enable
    kerberos_keytab: str  # Kerberos keytab setting. | MaxLen: 35
    domain_controller: str  # Domain controller setting. | MaxLen: 35
    saml_server: str  # SAML configuration. | MaxLen: 35
    saml_timeout: int  # SAML authentication timeout in seconds. | Default: 120 | Min: 30 | Max: 1200
    fsso_agent_for_ntlm: str  # FSSO agent to use for NTLM authentication. | MaxLen: 35
    require_tfa: Literal["enable", "disable"]  # Enable/disable two-factor authentication | Default: disable
    fsso_guest: Literal["enable", "disable"]  # Enable/disable user fsso-guest authentication | Default: disable
    user_cert: Literal["enable", "disable"]  # Enable/disable authentication with user certificat | Default: disable
    cert_http_header: Literal["enable", "disable"]  # Enable/disable authentication with user certificat | Default: disable
    user_database: list[dict[str, Any]]  # Authentication server to contain user information;
    ssh_ca: str  # SSH CA name. | MaxLen: 35
    external_idp: str  # External identity provider configuration. | MaxLen: 35
    group_attr_type: Literal["display-name", "external-id"]  # Group attribute type used to match SCIM groups | Default: display-name
    digest_algo: Literal["md5", "sha-256"]  # Digest Authentication Algorithms. | Default: md5 sha-256
    digest_rfc2069: Literal["enable", "disable"]  # Enable/disable support for the deprecated RFC2069 | Default: disable

# Nested TypedDicts for table field children (dict mode)

class SchemeUserdatabaseItem(TypedDict):
    """Type hints for user-database table item fields (dict mode).
    
    Provides IDE autocomplete for nested table field items.
    All fields are present in API responses.
    """
    
    name: str  # Authentication server name. | MaxLen: 79


# Nested classes for table field children (object mode)

@final
class SchemeUserdatabaseObject:
    """Typed object for user-database table items.
    
    Provides IDE autocomplete for nested table field attributes.
    At runtime, this is a FortiObject instance.
    """
    
    # Authentication server name. | MaxLen: 79
    name: str
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> dict[str, Any]: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...



# Response TypedDict for GET returns (all fields present in API response)
class SchemeResponse(TypedDict):
    """
    Type hints for authentication/scheme API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # Authentication scheme name. | MaxLen: 35
    method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"]  # Authentication methods (default = basic).
    negotiate_ntlm: Literal["enable", "disable"]  # Enable/disable negotiate authentication for NTLM | Default: enable
    kerberos_keytab: str  # Kerberos keytab setting. | MaxLen: 35
    domain_controller: str  # Domain controller setting. | MaxLen: 35
    saml_server: str  # SAML configuration. | MaxLen: 35
    saml_timeout: int  # SAML authentication timeout in seconds. | Default: 120 | Min: 30 | Max: 1200
    fsso_agent_for_ntlm: str  # FSSO agent to use for NTLM authentication. | MaxLen: 35
    require_tfa: Literal["enable", "disable"]  # Enable/disable two-factor authentication | Default: disable
    fsso_guest: Literal["enable", "disable"]  # Enable/disable user fsso-guest authentication | Default: disable
    user_cert: Literal["enable", "disable"]  # Enable/disable authentication with user certificat | Default: disable
    cert_http_header: Literal["enable", "disable"]  # Enable/disable authentication with user certificat | Default: disable
    user_database: list[SchemeUserdatabaseItem]  # Authentication server to contain user information;
    ssh_ca: str  # SSH CA name. | MaxLen: 35
    external_idp: str  # External identity provider configuration. | MaxLen: 35
    group_attr_type: Literal["display-name", "external-id"]  # Group attribute type used to match SCIM groups | Default: display-name
    digest_algo: Literal["md5", "sha-256"]  # Digest Authentication Algorithms. | Default: md5 sha-256
    digest_rfc2069: Literal["enable", "disable"]  # Enable/disable support for the deprecated RFC2069 | Default: disable


@final
class SchemeObject:
    """Typed FortiObject for authentication/scheme with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # Authentication scheme name. | MaxLen: 35
    name: str
    # Authentication methods (default = basic).
    method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"]
    # Enable/disable negotiate authentication for NTLM | Default: enable
    negotiate_ntlm: Literal["enable", "disable"]
    # Kerberos keytab setting. | MaxLen: 35
    kerberos_keytab: str
    # Domain controller setting. | MaxLen: 35
    domain_controller: str
    # SAML configuration. | MaxLen: 35
    saml_server: str
    # SAML authentication timeout in seconds. | Default: 120 | Min: 30 | Max: 1200
    saml_timeout: int
    # FSSO agent to use for NTLM authentication. | MaxLen: 35
    fsso_agent_for_ntlm: str
    # Enable/disable two-factor authentication (default = disable) | Default: disable
    require_tfa: Literal["enable", "disable"]
    # Enable/disable user fsso-guest authentication | Default: disable
    fsso_guest: Literal["enable", "disable"]
    # Enable/disable authentication with user certificate | Default: disable
    user_cert: Literal["enable", "disable"]
    # Enable/disable authentication with user certificate in Clien | Default: disable
    cert_http_header: Literal["enable", "disable"]
    # Authentication server to contain user information; "local-us
    user_database: list[SchemeUserdatabaseObject]
    # SSH CA name. | MaxLen: 35
    ssh_ca: str
    # External identity provider configuration. | MaxLen: 35
    external_idp: str
    # Group attribute type used to match SCIM groups | Default: display-name
    group_attr_type: Literal["display-name", "external-id"]
    # Digest Authentication Algorithms. | Default: md5 sha-256
    digest_algo: Literal["md5", "sha-256"]
    # Enable/disable support for the deprecated RFC2069 Digest Cli | Default: disable
    digest_rfc2069: Literal["enable", "disable"]
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> SchemePayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class Scheme:
    """
    Configure Authentication Schemes.
    
    Path: authentication/scheme
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
    ) -> SchemeResponse: ...
    
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
    ) -> SchemeResponse: ...
    
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
    ) -> list[SchemeResponse]: ...
    
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
    ) -> SchemeObject: ...
    
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
    ) -> SchemeObject: ...
    
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
    ) -> list[SchemeObject]: ...
    
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
    ) -> SchemeResponse: ...
    
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
    ) -> SchemeResponse: ...
    
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
    ) -> list[SchemeResponse]: ...
    
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
    ) -> SchemeObject | list[SchemeObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SchemeObject: ...
    
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SchemeObject: ...
    
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
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
    ) -> SchemeObject: ...
    
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
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
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

class SchemeDictMode:
    """Scheme endpoint for dict response mode (default for this client).
    
    By default returns SchemeResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return SchemeObject.
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
    ) -> SchemeObject: ...
    
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
    ) -> list[SchemeObject]: ...
    
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
    ) -> SchemeResponse: ...
    
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
    ) -> list[SchemeResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SchemeObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SchemeObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
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
    ) -> SchemeObject: ...
    
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
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
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


class SchemeObjectMode:
    """Scheme endpoint for object response mode (default for this client).
    
    By default returns SchemeObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return SchemeResponse (TypedDict).
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
    ) -> SchemeResponse: ...
    
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
    ) -> list[SchemeResponse]: ...
    
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
    ) -> SchemeObject: ...
    
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
    ) -> list[SchemeObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SchemeObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SchemeObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> SchemeObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SchemeObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
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
    ) -> SchemeObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> SchemeObject: ...
    
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
        payload_dict: SchemePayload | None = ...,
        name: str | None = ...,
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = ...,
        negotiate_ntlm: Literal["enable", "disable"] | None = ...,
        kerberos_keytab: str | None = ...,
        domain_controller: str | None = ...,
        saml_server: str | None = ...,
        saml_timeout: int | None = ...,
        fsso_agent_for_ntlm: str | None = ...,
        require_tfa: Literal["enable", "disable"] | None = ...,
        fsso_guest: Literal["enable", "disable"] | None = ...,
        user_cert: Literal["enable", "disable"] | None = ...,
        cert_http_header: Literal["enable", "disable"] | None = ...,
        user_database: str | list[str] | list[dict[str, Any]] | None = ...,
        ssh_ca: str | None = ...,
        external_idp: str | None = ...,
        group_attr_type: Literal["display-name", "external-id"] | None = ...,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = ...,
        digest_rfc2069: Literal["enable", "disable"] | None = ...,
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
    "Scheme",
    "SchemeDictMode",
    "SchemeObjectMode",
    "SchemePayload",
    "SchemeObject",
]