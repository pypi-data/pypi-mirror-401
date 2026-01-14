from typing import TypedDict, Literal, NotRequired, Any, Coroutine, Union, overload, Generator, final
from hfortix_fortios.models import FortiObject
from hfortix_core.types import MutationResponse, RawAPIResponse

# Payload TypedDict for IDE autocomplete (for POST/PUT - fields are optional via total=False)
# NOTE: We intentionally DON'T use NotRequired wrapper because:
# 1. total=False already makes all fields optional
# 2. NotRequired[Literal[...]] prevents Pylance from validating Literal values in dict literals
class WebPortalPayload(TypedDict, total=False):
    """
    Type hints for ztna/web_portal payload fields.
    
    Configure ztna web-portal.
    
    **Related Resources:**

    Dependencies (resources this endpoint references):
        - :class:`~.authentication.rule.RuleEndpoint` (via: auth-rule)
        - :class:`~.firewall.access-proxy-virtual-host.AccessProxyVirtualHostEndpoint` (via: auth-virtual-host, host)
        - :class:`~.firewall.decrypted-traffic-mirror.DecryptedTrafficMirrorEndpoint` (via: decrypted-traffic-mirror)
        - :class:`~.firewall.vip.VipEndpoint` (via: vip)
        - :class:`~.firewall.vip6.Vip6Endpoint` (via: vip6)

    **Usage:**
        payload: WebPortalPayload = {
            "field": "value",  # <- autocomplete shows all fields
        }
    """
    name: str  # ZTNA proxy name. | MaxLen: 79
    vip: str  # Virtual IP name. | MaxLen: 79
    host: str  # Virtual or real host name. | MaxLen: 79
    decrypted_traffic_mirror: str  # Decrypted traffic mirror. | MaxLen: 35
    log_blocked_traffic: Literal["disable", "enable"]  # Enable/disable logging of blocked traffic. | Default: enable
    auth_portal: Literal["disable", "enable"]  # Enable/disable authentication portal. | Default: disable
    auth_virtual_host: str  # Virtual host for authentication portal. | MaxLen: 79
    vip6: str  # Virtual IPv6 name. | MaxLen: 79
    auth_rule: str  # Authentication Rule. | MaxLen: 35
    display_bookmark: Literal["enable", "disable"]  # Enable to display the web portal bookmark widget. | Default: enable
    focus_bookmark: Literal["enable", "disable"]  # Enable to prioritize the placement of the bookmark | Default: disable
    display_status: Literal["enable", "disable"]  # Enable to display the web portal status widget. | Default: enable
    display_history: Literal["enable", "disable"]  # Enable to display the web portal user login histor | Default: disable
    policy_auth_sso: Literal["enable", "disable"]  # Enable policy sso authentication. | Default: enable
    heading: str  # Web portal heading message. | Default: ZTNA Portal | MaxLen: 31
    theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"]  # Web portal color scheme. | Default: security-fabric
    clipboard: Literal["enable", "disable"]  # Enable to support RDP/VPC clipboard functionality. | Default: enable
    default_window_width: int  # Screen width | Default: 1024 | Min: 0 | Max: 65535
    default_window_height: int  # Screen height | Default: 768 | Min: 0 | Max: 65535
    cookie_age: int  # Time in minutes that client web browsers should ke | Default: 60 | Min: 0 | Max: 525600
    forticlient_download: Literal["enable", "disable"]  # Enable/disable download option for FortiClient. | Default: enable
    customize_forticlient_download_url: Literal["enable", "disable"]  # Enable support of customized download URL for Fort | Default: disable
    windows_forticlient_download_url: str  # Download URL for Windows FortiClient. | MaxLen: 1023
    macos_forticlient_download_url: str  # Download URL for Mac FortiClient. | MaxLen: 1023

# Nested TypedDicts for table field children (dict mode)

# Nested classes for table field children (object mode)


# Response TypedDict for GET returns (all fields present in API response)
class WebPortalResponse(TypedDict):
    """
    Type hints for ztna/web_portal API response fields.
    
    All fields are present in the response from the FortiGate API.
    """
    name: str  # ZTNA proxy name. | MaxLen: 79
    vip: str  # Virtual IP name. | MaxLen: 79
    host: str  # Virtual or real host name. | MaxLen: 79
    decrypted_traffic_mirror: str  # Decrypted traffic mirror. | MaxLen: 35
    log_blocked_traffic: Literal["disable", "enable"]  # Enable/disable logging of blocked traffic. | Default: enable
    auth_portal: Literal["disable", "enable"]  # Enable/disable authentication portal. | Default: disable
    auth_virtual_host: str  # Virtual host for authentication portal. | MaxLen: 79
    vip6: str  # Virtual IPv6 name. | MaxLen: 79
    auth_rule: str  # Authentication Rule. | MaxLen: 35
    display_bookmark: Literal["enable", "disable"]  # Enable to display the web portal bookmark widget. | Default: enable
    focus_bookmark: Literal["enable", "disable"]  # Enable to prioritize the placement of the bookmark | Default: disable
    display_status: Literal["enable", "disable"]  # Enable to display the web portal status widget. | Default: enable
    display_history: Literal["enable", "disable"]  # Enable to display the web portal user login histor | Default: disable
    policy_auth_sso: Literal["enable", "disable"]  # Enable policy sso authentication. | Default: enable
    heading: str  # Web portal heading message. | Default: ZTNA Portal | MaxLen: 31
    theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"]  # Web portal color scheme. | Default: security-fabric
    clipboard: Literal["enable", "disable"]  # Enable to support RDP/VPC clipboard functionality. | Default: enable
    default_window_width: int  # Screen width | Default: 1024 | Min: 0 | Max: 65535
    default_window_height: int  # Screen height | Default: 768 | Min: 0 | Max: 65535
    cookie_age: int  # Time in minutes that client web browsers should ke | Default: 60 | Min: 0 | Max: 525600
    forticlient_download: Literal["enable", "disable"]  # Enable/disable download option for FortiClient. | Default: enable
    customize_forticlient_download_url: Literal["enable", "disable"]  # Enable support of customized download URL for Fort | Default: disable
    windows_forticlient_download_url: str  # Download URL for Windows FortiClient. | MaxLen: 1023
    macos_forticlient_download_url: str  # Download URL for Mac FortiClient. | MaxLen: 1023


@final
class WebPortalObject:
    """Typed FortiObject for ztna/web_portal with IDE autocomplete support.
    
    This is a typed wrapper that provides IDE autocomplete for API response fields.
    At runtime, this is actually a FortiObject instance.
    """
    
    # ZTNA proxy name. | MaxLen: 79
    name: str
    # Virtual IP name. | MaxLen: 79
    vip: str
    # Virtual or real host name. | MaxLen: 79
    host: str
    # Decrypted traffic mirror. | MaxLen: 35
    decrypted_traffic_mirror: str
    # Enable/disable logging of blocked traffic. | Default: enable
    log_blocked_traffic: Literal["disable", "enable"]
    # Enable/disable authentication portal. | Default: disable
    auth_portal: Literal["disable", "enable"]
    # Virtual host for authentication portal. | MaxLen: 79
    auth_virtual_host: str
    # Virtual IPv6 name. | MaxLen: 79
    vip6: str
    # Authentication Rule. | MaxLen: 35
    auth_rule: str
    # Enable to display the web portal bookmark widget. | Default: enable
    display_bookmark: Literal["enable", "disable"]
    # Enable to prioritize the placement of the bookmark section o | Default: disable
    focus_bookmark: Literal["enable", "disable"]
    # Enable to display the web portal status widget. | Default: enable
    display_status: Literal["enable", "disable"]
    # Enable to display the web portal user login history widget. | Default: disable
    display_history: Literal["enable", "disable"]
    # Enable policy sso authentication. | Default: enable
    policy_auth_sso: Literal["enable", "disable"]
    # Web portal heading message. | Default: ZTNA Portal | MaxLen: 31
    heading: str
    # Web portal color scheme. | Default: security-fabric
    theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"]
    # Enable to support RDP/VPC clipboard functionality. | Default: enable
    clipboard: Literal["enable", "disable"]
    # Screen width (range from 0 - 65535, default = 1024). | Default: 1024 | Min: 0 | Max: 65535
    default_window_width: int
    # Screen height (range from 0 - 65535, default = 768). | Default: 768 | Min: 0 | Max: 65535
    default_window_height: int
    # Time in minutes that client web browsers should keep a cooki | Default: 60 | Min: 0 | Max: 525600
    cookie_age: int
    # Enable/disable download option for FortiClient. | Default: enable
    forticlient_download: Literal["enable", "disable"]
    # Enable support of customized download URL for FortiClient. | Default: disable
    customize_forticlient_download_url: Literal["enable", "disable"]
    # Download URL for Windows FortiClient. | MaxLen: 1023
    windows_forticlient_download_url: str
    # Download URL for Mac FortiClient. | MaxLen: 1023
    macos_forticlient_download_url: str
    
    # Common API response fields
    status: str
    http_status: int | None
    vdom: str | None
    
    # Methods from FortiObject
    def get_full(self, name: str) -> Any: ...
    def to_dict(self) -> WebPortalPayload: ...
    def keys(self) -> Any: ...
    def values(self) -> Generator[Any, None, None]: ...
    def items(self) -> Generator[tuple[str, Any], None, None]: ...
    def get(self, key: str, default: Any = None) -> Any: ...
    def __getitem__(self, key: str) -> Any: ...


class WebPortal:
    """
    Configure ztna web-portal.
    
    Path: ztna/web_portal
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
    ) -> WebPortalResponse: ...
    
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
    ) -> WebPortalResponse: ...
    
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
    ) -> list[WebPortalResponse]: ...
    
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
    ) -> WebPortalObject: ...
    
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
    ) -> WebPortalObject: ...
    
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
    ) -> list[WebPortalObject]: ...
    
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
    ) -> WebPortalResponse: ...
    
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
    ) -> WebPortalResponse: ...
    
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
    ) -> list[WebPortalResponse]: ...
    
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
    ) -> WebPortalObject | list[WebPortalObject] | dict[str, Any] | list[dict[str, Any]]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> dict[str, Any]: ...
    
    # POST overloads
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WebPortalObject: ...
    
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: bool = ...,
        response_mode: Literal["dict", "object"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT overloads
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WebPortalObject: ...
    
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[False] = ...,
        response_mode: Literal["dict"] | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns the full API envelope
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # Default overload (no response_mode or raw_json specified)
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
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
    ) -> WebPortalObject: ...
    
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
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
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

class WebPortalDictMode:
    """WebPortal endpoint for dict response mode (default for this client).
    
    By default returns WebPortalResponse (TypedDict).
    Can be overridden per-call with response_mode="object" to return WebPortalObject.
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
    ) -> WebPortalObject: ...
    
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
    ) -> list[WebPortalObject]: ...
    
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
    ) -> WebPortalResponse: ...
    
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
    ) -> list[WebPortalResponse]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Object mode override
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WebPortalObject: ...
    
    # POST - Default overload (returns MutationResponse)
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Dict mode (default for DictMode class)
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WebPortalObject: ...
    
    # PUT - Default overload (returns MutationResponse)
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # PUT - Dict mode (default for DictMode class)
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
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
    ) -> WebPortalObject: ...
    
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
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
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


class WebPortalObjectMode:
    """WebPortal endpoint for object response mode (default for this client).
    
    By default returns WebPortalObject (FortiObject).
    Can be overridden per-call with response_mode="dict" to return WebPortalResponse (TypedDict).
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
    ) -> WebPortalResponse: ...
    
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
    ) -> list[WebPortalResponse]: ...
    
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
    ) -> WebPortalObject: ...
    
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
    ) -> list[WebPortalObject]: ...

    # raw_json=True returns RawAPIResponse for POST
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # POST - Dict mode override
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # POST - Object mode override (requires explicit response_mode="object")
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WebPortalObject: ...
    
    # POST - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> WebPortalObject: ...
    
    # POST - Default for ObjectMode (returns MutationResponse like DictMode)
    def post(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> MutationResponse: ...

    # PUT - Dict mode override
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["dict"],
        **kwargs: Any,
    ) -> MutationResponse: ...
    
    # raw_json=True returns RawAPIResponse for PUT
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        raw_json: Literal[True],
        **kwargs: Any,
    ) -> RawAPIResponse: ...
    
    # PUT - Object mode override (requires explicit response_mode="object")
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        *,
        response_mode: Literal["object"],
        **kwargs: Any,
    ) -> WebPortalObject: ...
    
    # PUT - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> WebPortalObject: ...
    
    # PUT - Default for ObjectMode (returns MutationResponse like DictMode)
    def put(
        self,
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
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
    ) -> WebPortalObject: ...
    
    # DELETE - Default overload (no response_mode specified, returns Object for ObjectMode)
    @overload
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> WebPortalObject: ...
    
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
        payload_dict: WebPortalPayload | None = ...,
        name: str | None = ...,
        vip: str | None = ...,
        host: str | None = ...,
        decrypted_traffic_mirror: str | None = ...,
        log_blocked_traffic: Literal["disable", "enable"] | None = ...,
        auth_portal: Literal["disable", "enable"] | None = ...,
        auth_virtual_host: str | None = ...,
        vip6: str | None = ...,
        auth_rule: str | None = ...,
        display_bookmark: Literal["enable", "disable"] | None = ...,
        focus_bookmark: Literal["enable", "disable"] | None = ...,
        display_status: Literal["enable", "disable"] | None = ...,
        display_history: Literal["enable", "disable"] | None = ...,
        policy_auth_sso: Literal["enable", "disable"] | None = ...,
        heading: str | None = ...,
        theme: Literal["jade", "neutrino", "mariner", "graphite", "melongene", "jet-stream", "security-fabric", "dark-matter", "onyx", "eclipse"] | None = ...,
        clipboard: Literal["enable", "disable"] | None = ...,
        default_window_width: int | None = ...,
        default_window_height: int | None = ...,
        cookie_age: int | None = ...,
        forticlient_download: Literal["enable", "disable"] | None = ...,
        customize_forticlient_download_url: Literal["enable", "disable"] | None = ...,
        windows_forticlient_download_url: str | None = ...,
        macos_forticlient_download_url: str | None = ...,
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
    "WebPortal",
    "WebPortalDictMode",
    "WebPortalObjectMode",
    "WebPortalPayload",
    "WebPortalObject",
]